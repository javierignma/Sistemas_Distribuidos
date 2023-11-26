import wikipediaapi as wp

Wiki_object = wp.Wikipedia('Tarea3SD (javier.molina@mail.udp.cl)', 'es')

with open('pages.txt') as f:
    counter = 1
    for line in f:
        page = line.replace(' ', '_').strip()
        page = Wiki_object.page(page).text
        page = page.replace("\n", " ")
        if counter < 16:
            with open('carpeta1/'+str(counter)+'.txt', 'w') as folder:
                folder.write(f'{line.replace(" ", "_").strip()}<splittername>"{page}"')
        else:
            with open('carpeta2/'+str(counter)+'.txt', 'w') as folder:
                folder.write(f'{line.replace(" ", "_").strip()}<splittername>"{page}"')
        print(f'Documento {counter}/30')
        counter += 1