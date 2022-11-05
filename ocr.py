import pytesseract
import re
import cv2
import nltk
from nltk import word_tokenize, pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# 17, 20, 23, 26

class extractInfo:
    def __init__(self, img_path) -> None:
        self.img = cv2.imread(img_path)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # Threshold
        # threshold, self.img = cv2.threshold(self.img, 127, 255, cv2.THRESH_BINARY)
        self.img = cv2.resize(self.img, (1080, 720), interpolation=cv2.INTER_LINEAR)

        # Extracting text from an image
        self.info = pytesseract.image_to_string(self.img)

    # name extraction
    def extract_name(self):
        info = self.info
        name = []
        for line in info.split('\n'):
            tokens = word_tokenize(line)
            tag = pos_tag(tokens)
            ne_tree = nltk.ne_chunk(tag)
            for subtree in ne_tree.subtrees():
                if subtree.label() == 'PERSON':
                    name.append(' '.join([sub_subtree[0] for sub_subtree in subtree]))
        return name

    # email extraction
    def extract_email(self):
        info = self.info
        result = [' '.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", line)) 
                for line in info.split('\n')
                if len(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", line)) != 0]
        return result

    # contact number extraction
    def extract_contact_number(self):
        info = self.info
        mob_num = [' '.join(re.findall('(\(\d{3}\)-\d{3}-\d{3}|\d{3}-\d{3}-\d{4}|\+\d{2}\d{10}|\d{10})', line))
                    for line in info.split('\n')
                    if len(re.findall('(\(\d{3}\)-\d{3}-\d{3}|\d{3}-\d{3}-\d{4}|\+\d{2}\d{10}|\d{10})', line)) != 0]
        return mob_num