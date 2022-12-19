from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from flask import Flask, request, render_template, send_file

app = Flask(__name__)

items = []

# Register the font with the reportlab library
pdfmetrics.registerFont(TTFont('ArialHebrew', 'fonts/arial-hebrew.ttf'))

def create_pdf_offer(title, subtitle, elements, header_image, mail, phone, file_name):
    print("Elements: ", elements)
    title = title[::-1]
    # Create a canvas with A4 page size
    canvas = Canvas(file_name, pagesize=A4)

    # Set the font and font size for the title
    canvas.setFont('ArialHebrew', 24)
    # Draw the title at the top of the page, aligning it to the center
    canvas.drawCentredString(A4[0] / 2, A4[1] - 1 * inch, title)

    # Set the font and font size for the subtitle
    canvas.setFont('ArialHebrew', 18)
    # Draw the subtitle below the title, aligning it to the center
    canvas.drawCentredString(A4[0] / 2, A4[1] - 1.5 * inch, subtitle)

    # Draw the header image at the top of the page
    # Calculate the horizontal center of the page
    x = A4[0] / 2
    # Set the top margin of the page
    y = A4[1] - 1 * inch

    # Draw the header image at the top center of the page
    canvas.drawImage(ImageReader(header_image), x=x, y=y, width=6 * inch, height=1 * inch, preserveAspectRatio=True)
    # Set the font and font size for the elements
    canvas.setFont('ArialHebrew', 14)
    # Initialize the vertical position for the elements
    y = A4[1] - 4 * inch
    # Iterate over the elements and draw them on the canvas
    total = 0
    for element in elements:
        # Split the element into description and price
        description, price = element.split(':')
        total+=int(price)
        # Draw the description
        canvas.drawString(1 * inch, y, price + "₪")
        # Draw the price aligned to the right of the page
        canvas.drawRightString(A4[0] - 1 * inch, y, description[::-1])
        # Decrement the vertical position for the next element
        y -= 0.2 * inch

    canvas.drawRightString(1*inch, y, f"{total}₪   ")

    # Set the font and font size for the footer
    canvas.setFont('Helvetica', 12)
    # Draw the mail in the bottom left corner of the page
    canvas.drawString(1 * inch, 1 * inch, mail)
    # Draw the phone in the bottom right corner of the page
    canvas.drawRightString(A4[0] - 1 * inch, 1 * inch, phone)

    # Save the canvas to the PDF file
    canvas.save()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        description = request.form['description']
        price = request.form['price']
        items.append({'description': description, 'price': price})

    return render_template('index.html', items=items)

@app.route('/save', methods=['POST'])
def save():
    its = []
    for item in items:
        desc = item["description"]
        price = item["price"]
        its.append(f"{desc}:{price}")
    create_pdf_offer("יגאל מערכות","0523430888",its,"logo.jpeg", "ilay778899@gmail.com", "0523430888", "offer.pdf")
    file_path = 'offer.pdf'

    # Send the file to the user
    return send_file(file_path, as_attachment=True)
    #return 'Saved'

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")

#create_pdf_offer("יגאל מערכות","0523430888",["התקנת מזגן:1200","בלה בלהגשד :10","גדשגדש גשדגדש:10"],"logo.jpeg", "ilay778899@gmail.com", "0523430888", "doc.pdf")
