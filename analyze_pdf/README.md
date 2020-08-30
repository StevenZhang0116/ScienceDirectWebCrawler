# Analyze PDF contents

In the analyze_text.py file, I use pdfminer package to convert PDF contents by page into the JSON file, also handle the exceptional errors from Unicode transformations. 

In pdfminer_tester.py file, I propose a general outline of the idea to automatically identify and extract figures/tables/entities from the paper by analyzing the formats of the documents (e.g, text arrangments and vertical/horizontal lines). I use different color frames to highlight their locations and pull out the content. However, the accuracy is relevant to low, so the code is still a semi-manufacture. (Noteworthy, the Semantic Scholar website accomplishes that goal successfully and elegantly using computer vision. Another app named ReadIris could also scan and extract the relevant contents from pdfs into editable files (xlsx, doc, etc.))
