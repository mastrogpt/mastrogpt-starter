import sys
from pathlib import Path
import csv

if len(sys.argv) < 2:
    print("please specify the path of a Linkedin Connections.csv file")
    sys.exit(0)

#filein = "Connections.csv"
filein = sys.argv[1]
fileout = filein.rsplit(".",1)[0] + ".txt"

#file = open(filein)
with open(filein) as file:

    #lines = Path(filein).read_text().split("\n")
    reader = csv.reader(file)
    # skip empty lines
    next(reader) ; next(reader) ; next(reader)
    header = next(reader)
    res = ""
    count = 0
    for line in reader:
        try:
            [name, surname, url, email, company, job, connected] = line
            if name + surname == "": 
                continue
        except:
            print("\nskip", line)
            continue

        sent = f"- The contact {name} {surname}"
        sent += f" has the role {job}" if job else ""
        sent += f" works at the company {company}" if company else ""
        sent += f" his email address is {email}" if email else ""
        sent += f" his linkedin page is {url}" if {url} else ""
        sent += ".\n" 
        print(".", end='')
        res += sent
        count += 1
        if count % 100 == 0: print() ; print(count, end='')
 
Path(fileout).write_text(res)
print(f"\n*** saved {fileout}")


   