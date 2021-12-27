from json import load

checklist_add = []

# True = Error
def configCheck():
    if __name__ == "__main__":
        config = load(open('../config.json'))
    else:
        config = load(open('config.json'))
    if config['api_key'] == "" or config['api_url'] == "":
        print("\033[91mMangler API nøkkel eller API url\033[0m")
        return True
    return False


def checklist_main():
    checklist_reserved = [configCheck]
    errors = 0
    checked = 0
    for funk in checklist_reserved + checklist_add:
        if funk(): errors = errors + 1
        checked = checked + 1
    print(f"\n\033[92m{checked} modul(er) sjekket.\033[91m {errors} feil oppdaget.\033[0m")


if __name__ == "__main__":
    checklist_main()