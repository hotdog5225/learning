import os

import pdfcrowd
import sys
import pdfkit
from concurrent.futures import ThreadPoolExecutor, as_completed

def getPdf(url, name):
    pdfkit.from_url(url, name)
    return name

getPdf("https://www.learncpp.com/cpp-tutorial/forward-declarations/", "2.6 — Forward declarations and definitions.pdf")
sys.exit()

f = open("urls.txt")

with ThreadPoolExecutor(max_workers=10) as t:
    task_list = []
    line = f.readline()

    while line:
        # get name
        lineText = line.split("\t")
        name = (lineText[0] +"_"+ lineText[1]).replace("/", "_") + ".pdf"
        if os.path.exists(name):
            line = f.readline()
            print("exist: ", name)
        # get url
        url = lineText[2]

        # get pdf
        task_list.append(t.submit(getPdf, url, name))

        line = f.readline()

    for future in as_completed(task_list):
        data = future.result()
        print(f"DONE: {data}")

f.close()

sys.exit()


try:
    # create the API client instance
    client = pdfcrowd.HtmlToPdfClient('hotdog5225', 'b5b7e209b1f225c2771a26818d950226')

    # configure the conversion
    client.setNoMargins(True)
    client.setFooterHtml("""<style>* {  margin: 0; padding: 0 }</style>
    <div style="background-color: grey; height: 100%;text-align:center;line-height: 0.3in; color: white;font-size: 1.3rem;vertical-align: middle;">
    page <span class='pdfcrowd-page-number'></span> of <span class='pdfcrowd-page-count'></span> pages
    </div>""")
    client.setNoHeaderFooterHorizontalMargins(True)
    # configure the conversion
    client.setHeaderHeight('15mm')
    client.setFooterHeight('10mm')
    client.setHeaderHtml('<a class=\'pdfcrowd-source-url\' data-pdfcrowd-placement=\'href-and-content\'></a>')
    client.setFooterHtml('<center><span class=\'pdfcrowd-page-number\'></span></center>')
    client.setMarginTop('0')
    client.setMarginBottom('0')
    client.setBlockAds(True)

except:
    # report the error
    sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))

    # rethrow or handle the exception
    raise


f = open("urls.txt")
line = f.readline()
while line:
    # get name
    lineText = line.split("\t")
    name = (lineText[0] +"_"+ lineText[1]).replace("/", "_") + ".pdf"
    if os.path.exists(name):
        line = f.readline()
        print("exist: ", name)
        continue

    url = lineText[2]

    # get pdf
    try:
        # run the conversion and write the result to a file
        client.convertUrlToFile(url, name)
    except pdfcrowd.Error as why:
        # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))

        # rethrow or handle the exception
        raise

    print("DONE: %s", name)

    line = f.readline()
f.close()

sys.exit(0)
