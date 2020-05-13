import os

mypath = os.path.join(os.getcwd(), "notebooks")
notebooks = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

text = open(os.path.join(os.getcwd(), "placeholders", "index_template.txt"), "r")
index_template = text.read()
text.close()

text = open(os.path.join(os.getcwd(), "placeholders", "box_template.txt"), "r")
box_template = text.read()
text.close()

all_boxes = []
counter = 1
for notebook in notebooks:
	if counter%3 == 0:
		new_box = box_template.replace("{title}", notebook.replace("_", " ")).replace("{file}", notebook.replace(".ipynb", "")).replace("tg-one-third", "tg-one-third tg-one-third-last")
	else:
		new_box = box_template.replace("{title}", notebook.replace("_", " ")).replace("{file}", notebook.replace(".ipynb", ""))
	all_boxes.append(new_box)
	counter += 1

all_boxes = "\n".join(all_boxes)
new_index = index_template.replace("{blocks}", all_boxes)

text = open("index.rst", "w")
text.write(new_index)
text.close()