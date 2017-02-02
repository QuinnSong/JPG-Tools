from PIL import Image
from StringIO import StringIO
from PyPDF2.merger import PdfFileMerger
from PyPDF2.pdf import PdfFileReader

img = Image.open("d:\\windows\\desktop\\canon.jpg")
fil1 = StringIO()
img.save(fil1, "PDF")
filenames = []
filenames.append(fil1)
print "start png"
img = Image.open("d:\\windows\\desktop\\t.png").convert("RGB")
print "img done"
fil1 = StringIO()
img.save(fil1, "PDF")
filenames.append(fil1)

merger = PdfFileMerger()
#filenames = ["c:\\1.pdf", "c:\\tmp.pdf"]

for f in filenames:
    print "looping"
    merger.append(PdfFileReader(StringIO(f.getvalue()), 'rb'))
print "writing to file"
merger.write("c:\\total.pdf")


#-----------------------------------------------------------
#import sys
#from PIL import Image
#from reportlab.lib.pagesizes import letter
#from reportlab.platypus import SimpleDocTemplate, flowables
#
#__jpgname = str()
#def drawPageFrame(canvas, doc):
#   
#    
#    width, height =  letter
#    canvas.saveState()
#    canvas.drawImage(
#    __jpgname, 0, 0, height, width,
#    preserveAspectRatio=True, anchor='c')
#    canvas.restoreState()
#
#def jpg2pdf(pdfname):
#    im = Image.open(__jpgname)
#    width, height = letter
#
#    # To make it landscape, pagesize is reversed
#    # You can modify the code to add PDF metadata if you want
#    doc = SimpleDocTemplate(pdfname, pagesize=(height, width))
#    elem = []
#
#    elem.append(flowables.Macro('canvas.saveState()'))
#    elem.append(flowables.Macro('canvas.restoreState()'))
#
#    doc.build(elem, onFirstPage=drawPageFrame)
#
#if __name__ == '__main__':
#    #if len(sys.argv) < 3:
#    #print("Usage: python jpg2pdf.py <jpgname> <pdfname>")
#    #exit(1)
#    #__jpgname = sys.argv[1]
#    #jpg2pdf(sys.argv[2])
#    __jpgname = "d:\\windows\\desktop\\canon.jpg"
#    jpg2pdf("c:\\1_1.pdf")
#----------------------------------------------