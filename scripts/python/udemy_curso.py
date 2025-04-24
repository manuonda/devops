from bs4 import BeautifulSoup
import textwrap

def clean_text(element):
    if element:
        return " ".join(element.get_text(separator=" ", strip=True).split())
    return "No disponible"

def wrap(text, width=80):
    return textwrap.fill(text, width=width)

# Leer archivo HTML
with open("archivo.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Buscar todas las preguntas
question_blocks = soup.find_all("div", class_="result-pane--question-result-pane-wrapper--2bGiz")

# Archivo de salida
with open("preguntas_para_impresion.txt", "w", encoding="utf-8") as output:

    for idx, block in enumerate(question_blocks, 1):
        output.write("=" * 80 + "\n")
        output.write(f"PREGUNTA {idx}\n")
        output.write("=" * 80 + "\n\n")

        # Pregunta
        question_div = block.find("div", id="question-prompt")
        question_text = clean_text(question_div)
        output.write("PREGUNTA:\n")
        output.write(wrap(question_text) + "\n\n")

        # Respuestas
        answer_divs = block.find_all("div", id="answer-text")
        answers = [clean_text(div) for div in answer_divs]
        output.write("RESPUESTAS:\n")
        for i, answer in enumerate(answers, 1):
            output.write(wrap(f"{i}. {answer}") + "\n")
        output.write("\n")

        # Respuesta correcta
        correct_answer_div = block.find("div", class_="answer-result-pane--answer-correct--PLOEU")
        correct_answer = ""
        if correct_answer_div:
            answer_body = correct_answer_div.find("div", id="answer-text")
            correct_answer = clean_text(answer_body)
        output.write("RESPUESTA CORRECTA:\n")
        output.write(wrap(correct_answer or 'No detectada') + "\n\n")

        # Explicación general con salto de línea después de cada <p>
        explanation_div = block.find("div", id="overall-explanation")
        output.write("EXPLICACIÓN GENERAL:\n")
        if explanation_div:
            paragraphs = explanation_div.find_all("p")
            for p in paragraphs:
                text = clean_text(p)
                output.write(wrap(text) + "\n\n")  # salto extra
        else:
            output.write("Sin explicación\n\n")

print("✅ Listo: archivo formateado con saltos de línea en explicaciones.")
