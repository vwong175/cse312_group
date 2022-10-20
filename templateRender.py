

def htmlRender(filename, data):

    with open(filename) as html_file:
        template = html_file.read()
        template = replacePlaceholders(template, data)
        template = renderLoop(template, data)
        return template

def replacePlaceholders(template,data):
    replaced = template
    for placeHolders in data.keys():
        if isinstance(data[placeHolders], str):
            replaced = replaced.replace("{{" + placeHolders + "}}", data[placeHolders])
    return replaced

def renderLoop(template, data):
    if "loopData" in data:
        startTag = "{{loop}}"
        endTag = "{{endLoop}}"

        startIndex = template.find(startTag)
        endIndex = template.find(endTag)

        newTemplate = template[startIndex + len(startTag): endIndex]
        newData = data["loopData"]

        loop_Content = ""
        for piece in newData:
            loop_Content += replacePlaceholders(newTemplate,piece)

        result = template[:startIndex] + loop_Content + template[endIndex + len(endTag):]

        return result
