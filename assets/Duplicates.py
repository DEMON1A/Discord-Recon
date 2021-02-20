# define globals
subdomainsList = []

def Duplicates(Subdomains):
    global subdomainsList

    Subdomains = Subdomains.split('\n')
    for singleSubdomain in Subdomains:
        if singleSubdomain not in subdomainsList:
            subdomainsList.append(singleSubdomain)
        else:
            pass

    return subdomainsList