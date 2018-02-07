#from . import helpers
from audio import core as A
from display import core as D
from omr import core as O

# Create image from PDF
#D.helpers.pdf_to_png('./data/Chopin Nocturne op9 no2.pdf', 200, './data')
png = './data/Chopin Nocturne op9 no2-001.png'

# Load GUI
D.qt_gui(A,O,png)
