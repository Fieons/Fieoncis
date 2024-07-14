with open("E:\\BaiduNetdiskDownload\\[OCR]_Hitchhiker's Guide to the Galaxy_20240713_2047.txt", 'r', encoding= 'utf-8') as f:
    contents = f.readlines()

new_contents = []

for content in contents:
    if "T H E  H I T C H H I K E R ' S  G U I D E  T O  T H E  G A L A X Y" in content:
        continue
    if "D O U G L A S  A D A M S" in content:
        continue
    if "≦" in content:
        continue
    if "\n" == content:
        continue
    else:
        new_contents.append(content)

contents = new_contents

new_contents = []
i=0
while i < len(contents):
    if any(char.isalpha() for char in contents[i][-3:]):
        new_contents.append(contents[i].replace("\n","")+contents[i+1])
        i+=1
    else:
        new_contents.append(contents[i])

    i+=1
contents = new_contents

print(contents)

with open("E:\\BaiduNetdiskDownload\\[OCR]_Hitchhiker's Guide to the Galaxy_20240713_2047_cleaned.md", 'w', encoding= 'utf-8') as f:
    f.writelines(contents)



