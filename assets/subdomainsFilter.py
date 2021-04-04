'''
this util is made to validate the subdomains getting added into the hosts
if they're like the main subdomain the program is scanning. then it should pass
otherwise it shouldn't return anything
'''

def vSubdomains(sList, huntingTarget):
    mainSubdomains = []

    for singleSubdomain in sList:
        if singleSubdomain[-len(huntingTarget):] == huntingTarget:
            mainSubdomains.append(singleSubdomain)
        else:
            pass

    return mainSubdomains
