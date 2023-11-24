import wikipediaapi as wp

Wiki_object = wp.Wikipedia('Tarea3SD (javier.molina@mail.udp.cl)', 'es')

with open('pages.txt') as f:
    counter = 1
    for line in f:
        page = line.replace(' ', '_').strip()
        page = Wiki_object.page(page).text
        if counter < 16:
            with open('[1-15]/Documento'+str(counter)+'.txt', 'w') as folder:
                folder.write(page)
        else:
            with open('[16-30]/Documento'+str(counter)+'.txt', 'w') as folder:
                folder.write(page)
        print(f'Documento {counter}/30')
        counter += 1