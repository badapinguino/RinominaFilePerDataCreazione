import datetime
import os
import platform
import shutil
import glob
import time
import sys
from progressbar import progressbar

# Fai partire il timer per cronometrare l'esecuzione del programma
start_time = time.time()
# Print total number of arguments
print('Total number of arguments:', format(len(sys.argv)))

# Print all arguments
print('Argument List:', str(sys.argv))
percorsoFilesInput = ".\\"
percorsoFilesOutput = ".\\"
if len(sys.argv)>1:
    # Print arguments one by one
    for arg in sys.argv:
        print('Argument: ', str(arg))
    percorsoFilesInput = sys.argv[1]
    if not percorsoFilesInput.endswith('\\'):
        percorsoFilesInput = percorsoFilesInput + "\\"
    if len(sys.argv)>2:
        percorsoFilesOutput = sys.argv[2]
        if not percorsoFilesOutput.endswith('\\'):
            percorsoFilesOutput = percorsoFilesOutput + "\\"
    else:
        percorsoFilesOutput = percorsoFilesInput

print("PercorsoFilesInput: " + percorsoFilesInput)
print("PercorsoFilesOutput: " + percorsoFilesOutput)

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

# Directory
sottoCartella = "FileRinominati"

# Path
pathOut = os.path.join(percorsoFilesOutput, sottoCartella)

# Create the directory
if not os.path.exists(pathOut):
    os.mkdir(pathOut)
    print("Directory '% s' created" % sottoCartella)
else:
    print("Directory ", pathOut, " già esistente")

contatoreFile = 0
contatoreFileDoppi=0
os.chdir(percorsoFilesInput)
fileTotaliNellaCartella = glob.glob("*.*")
# creo la progress bar
for i in progressbar(range(len(fileTotaliNellaCartella)), redirect_stdout=True):
#for file in fileTotaliNellaCartella:
    file = fileTotaliNellaCartella[i]
    print()
    print('Esecuzione per file numero: ' + str(contatoreFile))
    print('File trovato: ' + file)
    estensioneFile = os.path.splitext(file)[1]
    #print('Estensione file appena trovato: ', estensioneFile)
    dataModifica = modification_date(percorsoFilesInput + file)
    print("Data modifica file " + file + ": ", dataModifica)
    pathAnno = pathOut+'\\'+str(dataModifica.year)
    if not os.path.exists(pathAnno):
        os.mkdir(pathAnno)
        print("Directory '% s' created" % pathAnno)
    else:
        print("Directory ", pathAnno, " già esistente")
    mese = dataModifica.month
    if mese > 0 & mese < 10:
        mese = '0' + str(mese)
    else:
        mese = str(mese)
    pathMese = pathAnno + '\\' + mese
    if not os.path.exists(pathMese):
        os.mkdir(pathMese)
        print("Directory '% s' created" % pathMese)
    else:
        print("Directory ", pathMese, " già esistente")
    try:
        nomeFileOutput = pathMese + '\\File_' + dataModifica.strftime('%Y%m%d-%H%M%S') + estensioneFile
        if not os.path.exists(nomeFileOutput):
            pathRisultato = shutil.copy2(percorsoFilesInput + file, nomeFileOutput)
            print('File copiato in: ' + pathRisultato)
        else:
            pathRisultato = shutil.copy2(percorsoFilesInput + file, pathMese + '\\File_' + dataModifica.strftime('%Y%m%d-%H%M%S') + '_' + str(contatoreFileDoppi) +  estensioneFile)
            print('File (doppio numero: ' + str(contatoreFileDoppi) + ') copiato in: ' + pathRisultato)
            contatoreFileDoppi = contatoreFileDoppi + 1
    except shutil.Error as e:
        print('Shutil Error: %s' % e)
    except IOError as e:
        print('IOError: %s' % e.strerror)
    contatoreFile = contatoreFile + 1
    # fine ciclo

print()
print("--- Programma terminato. Numero file copiati: " + str(contatoreFile) + " ---")
print("--- Programma terminato. Tempo esecuzione: %s seconds ---" % (time.time() - start_time))
