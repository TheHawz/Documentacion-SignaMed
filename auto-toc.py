import os


def header_to_toc(line):
    import re
    parts = line.split()
    res = ''

    if parts[0] == '#':
        res = ''
    if parts[0] == '##':
        res = ''
    if parts[0] == '###':
        res = '\t- '
    if parts[0] == '####':
        res = '\t\t- '

    title = ' '.join(parts[1:])
    link = '-'.join(parts[1:]).lower()

    return f'{res}[{title}](#{link})'


# myDict = {"name": "John", "country": "Norway"}
# mySeparator = "TEST"

# x = mySeparator.join(myDict)

def main(file, levels=2):

    with open(file, encoding='utf-8') as fr:
        lines = fr.readlines()

        code_block = False

        toc_lines = []

        for line in lines:
            if line.startswith('```'):
                code_block = not code_block

            if code_block:
                continue

            if line.startswith('# '):
                # toc_lines.append(line)
                continue

            if levels < 2:
                continue
            if line.startswith('## '):
                toc_lines.append(line)
                continue

            if levels < 3:
                continue
            if line.startswith('### '):
                toc_lines.append(line)
                continue

            if levels < 4:
                continue
            if line.startswith('#### '):
                toc_lines.append(line)
                continue

        c = 1
        toc = []
        for line in toc_lines:
            link = header_to_toc(line)
            if (line.split()[0] == '##'):
                link = f'{c}. '+link
                c += 1
            toc.append(link)

        with open('res.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(toc))


if __name__ == '__main__':
    file = os.path.join('app/doc.md')
    main(file, levels=3)
