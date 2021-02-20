def removeString(BadText , Output):
    lines = []
    Output = Output.split('\n')

    for line in Output:
        if BadText in line.rstrip('\n'):
            pass
        else:
            lines.append(line + '\n')

    return ''.join(lines)