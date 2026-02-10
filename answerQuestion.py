from interfaces import MCQuestion, FillInBlank, Constellation
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Expect OPENAI_API_KEY in environment
openaikey = os.getenv("OPENAI_API_KEY")
if not openaikey:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable. Create a .env file or set it in your environment.")

client = OpenAI(api_key=openaikey)
debug = False

def solveMCQ(questionCont: MCQuestion):
    response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You must answer by outputting only a single letter: A, B, C, or D. Give no explanation—just the letter."
            },
            {
                "role": "user",
                "content": f'''{questionCont.question}
{questionCont.choices}'''
            }
        ],
        max_tokens=1,
        temperature=0)
    value = (response.choices[0].message.content.strip()[0])
    if debug: print("Successfully solved! Answer: ", value)
    return value

def solveFillInBlank(questionCont: FillInBlank):
    incorrectAnswers: list[str] = []
    max_attempts = 5  # safety cap

    base_prompt = (
        f"The answer is a single word, similar to: {questionCont.hint}, "
        f"begins with '{questionCont.firstLetter}', "
        f"and is exactly {questionCont.maxLength} letters long (not more, not less). The answer is NEVER a proper noun (ex: Minneapolis)"
        "If no English word fits, respond with 'none'. "
        "Add inflections to meet max length requirements if needed. (e.g., if the max length is 8 and your answer is 'parable', add the -s ending to make it 'parables'.)"
        "Do not explain. Only output the word."
    )

    try: # runs to correct the model incase it gets it wrong the first time
        for attempt in range(max_attempts):
            extra = ""
            if incorrectAnswers:
                extra = f" It is NOT any of these word(s): {incorrectAnswers}."

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You must answer with only a single word—no explanation or additional text.",
                    },
                    {
                        "role": "user",
                        "content": base_prompt + extra,
                    },
                ],
                max_tokens=questionCont.maxLength + 2,
                temperature=0,
            )

            content = response.choices[0].message.content if response.choices else ""
            print("Fill-in-the-blank answer received:", content, "\n")
            answer_split = content.strip().split()
            answer = answer_split[0] if answer_split else None

            if answer and len(answer) == questionCont.maxLength:
                return answer

            print(f"Rejected answer '{answer}' (length {len(answer) if answer else 'n/a'})")
            incorrectAnswers.append(answer)

        print(f"No valid answer after {max_attempts} attempts.")
        return None

    except Exception as e:
        print(f"solveFillInBlank error: {e}")
        return None


def solveConstellations(questionCont: Constellation):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You must answer with only a single letter representing the correct choice: "
                        "A, B, C, or D. Do not output anything else."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Given the question: {questionCont.question} "
                        f"and the options: {', '.join(questionCont.options)}, "
                        "respond with the single uppercase letter of the best answer."
                    ),
                },
            ],
            max_tokens=1,
            temperature=0,
        )
        content = response.choices[0].message.content.strip().upper() if response.choices else ""
        if content in {'A', 'B', 'C', 'D'}:
            return content
        else:
            print(f"Rejected answer '{content}' not in valid option letters.")
            return None
    except Exception as e:
        print(f"solveConstellations error: {e}")
        return None
