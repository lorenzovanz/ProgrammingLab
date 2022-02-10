from datetime import date

class ExamException(Exception):
    pass

#--------------------------------------------------------------------------------------------------------------------------------------------------

class CSVFile:
    def __init__(self, name):
        self.name = name

    #METODO CHE ESTRAE DAL FILE TUTTE LE COPPIE data-num_passseggeri
    def get_data(self):
        dati = []

        try:
            file = open(self.name, 'r')
            data_precedente = ''
            for linea in file:
            #leggo il file e man mano aggiungo a 'dati'
            
                if ',' in linea:
                    elementi = linea.split(",")
                    #sanitizzo i due campi
                    elementi[0] = elementi[0].strip()
                    elementi[1] = elementi[1].strip()

                    if elementi[0] != 'date':
                        #controllo i casi in cui ci sia il mese che vale 1 invecce di 01 ecc.
                        yy_mm = elementi[0].split('-')
                        yy = yy_mm[0].strip()
                        mm = yy_mm[1].strip()

                        if len(mm) == 1:
                            mm = '0'+ mm  
                        
                        elementi[0] = yy+'-'+mm 

                        elementi = [elementi[0], elementi[1]]
                        
                        if elementi[0] > data_precedente:
                            data_prec = data_precedente.split('-')
                            yy_prec = data_prec[0].strip()
                            mm_prec = data_prec[1].strip()

                            mm_prec = int(mm_prec)
                            mm = int(mm)

                            #controllo se mi trovo in una situazione in cui mancano gli ultimi mesi di un anno
                            #e i primi di quello successivo    
                            #es ->    '1949-06', '1950-03'

                            if yy_prec == yy:
                                if mm_prec == mm-1: 
                                    try:
                                        elementi[1] = int(elementi[1])
                                    except:
                                        elementi[1] = 0  

                                    dati.append(elementi)  
                                    data_precedente = elementi[0]

                                else:
                                    #caso in cui non ci siano proprio dei timestamp per alcuni mesi
                                    for i in range(mm_prec+1, mm):
                                        mm_da_aggiungere = ''
                                        if i<=9:
                                            mm_da_aggiungere+='0'+str(i)
                                        else:
                                            mm_da_aggiungere+=str(i)

                                        dati.append([yy+'-'+mm_da_aggiungere, 0])

                                    #aggiungo il valore n-esimo dei passeggeri
                                    try:
                                        elementi[1] = int(elementi[1])
                                    except:
                                        elementi[1] = 0
                                            
                                    dati.append(elementi)    
                                    data_precedente = elementi[0]    
                            else:
                                #ho due anni diversi
                                if mm_prec==12:
                                    #controllo se esiste gennaio dell'anno n-esimo o meno
                                    if mm == 1:
                                        try:
                                            elementi[1] = int(elementi[1])
                                        except:
                                            elementi[1] = 0  

                                        dati.append(elementi)
                                        data_precedente = elementi[0]  
                                    else:
                                        for i in range(1, mm):
                                            mm_da_aggiungere = ''
                                            if i<=9:
                                                mm_da_aggiungere+='0'+str(i)
                                            else:
                                                mm_da_aggiungere+=str(i)

                                            dati.append([yy+'-'+mm_da_aggiungere, 0]) 

                                        #aggiungo il valore n-esimo dei passeggeri
                                        try:
                                            elementi[1] = int(elementi[1])
                                        except:
                                            elementi[1] = 0    
                                        dati.append(elementi)    
                                        data_precedente = elementi[0]  
                                else:
                                    #sono in questo caso '1949-06', '1950-03'
                                    for i in range(mm_prec+1, 13):
                                        mm_da_aggiungere = ''
                                        if i<=9:
                                            mm_da_aggiungere+='0'+str(i)
                                        else:
                                            mm_da_aggiungere+=str(i)

                                        dati.append([yy_prec+'-'+mm_da_aggiungere, 0])

                                    if mm != 1:
                                        for i in range(1, mm):
                                            mm_da_aggiungere = ''
                                            if i<=9:
                                                mm_da_aggiungere+='0'+str(i)
                                            else:
                                                mm_da_aggiungere+=str(i)

                                            dati.append([yy+'-'+mm_da_aggiungere, 0]) 

                                    #aggiungo il valore n-esimo dei passeggeri
                                    try:
                                        elementi[1] = int(elementi[1])
                                    except:
                                        elementi[1] = 0    
                                    dati.append(elementi)    
                                    data_precedente = elementi[0]         
                        else:
                            raise ExamException('La serie temporale del file non è orinata!')        
                    else:
                        #leggo la prima linea del file e assegno alla variabile data_precedente la data letta
                        prima_linea = file.readline()
                        
                        while ',' not in prima_linea:
                            prima_linea = file.readline()
                      
                        if ',' in prima_linea:
                            elementi = prima_linea.split(",")
                            #sanitizzo i due campi
                            elementi[0] = elementi[0].strip()
                            elementi[1] = elementi[1].strip()
                            
                            yy_mm = elementi[0].split('-')
                            yy = yy_mm[0].strip()
                            mm = yy_mm[1].strip()

                            if len(mm) == 1:
                                mm = '0'+ mm  
                        
                            elementi[0] = yy+'-'+mm 

                            #controllo di partire dal mese di gennaio del primo anno, in caso contrario aggiungo i timpestamp
                            mm = int(mm)
                            if mm != 1:
                                for i in range(1, mm):
                                    mm_da_aggiungere = ''
                                    if i<=9:
                                        mm_da_aggiungere+='0'+str(i)
                                    else:
                                        mm_da_aggiungere+=str(i)

                                    dati.append([yy+'-'+mm_da_aggiungere, 0]) 

                            #aggiungo il valore n-esimo dei passeggeri
                            try:
                                elementi[1] = int(elementi[1])
                            except:
                                elementi[1] = 0    
                            dati.append(elementi)    
                            data_precedente = elementi[0]

            #controllo di non essere nel caso in cui manchi uno o più mesi alla fine del file       
            controllo_ultimo = dati[len(dati)-1][0].split(',')[0].split('-')
            ultimo = int(controllo_ultimo[1])
            
            if ultimo != 12:
                for i in range(ultimo+1, 13):
                    mm_da_aggiungere = ''
                    if i<=9:
                        mm_da_aggiungere+='0'+str(i)
                    else:
                        mm_da_aggiungere+=str(i)

                    dati.append([yy+'-'+mm_da_aggiungere, 0])

            return dati 
        except:
            raise ExamException('Il file non è leggibile!')  
             
#--------------------------------------------------------------------------------------------------------------------------------------------------      

#calcolo lla differenza media del numero di passeggeri mensili tra anni consecutivi

def compute_avg_monthly_difference(time_series, first_year, last_year):
    
    #CASI CONTROLLO SU first_year e last_year

    #sanitizzo first_year e last_year
    first_year = first_year.strip()
    last_year = last_year.strip()

    #controllo che siano presenti nel file first_year e last_year, in caso contrario alzo un eccezione
    indice_first_year=0
    data = time_series[indice_first_year][0].split('-')

    while indice_first_year<len(time_series)-1 and first_year != data[0].strip():
        indice_first_year+=1
        data = time_series[indice_first_year][0].split('-')

    #utlima data del file
    ultima_data = time_series[len(time_series)-1][0].split('-')
    ultimo_anno = ultima_data[0]
    print(indice_first_year)
    if indice_first_year==len(time_series)-1 or first_year>=last_year or last_year>ultimo_anno.strip():
        raise ExamException('Inserire dei valori validi per first_year e last_year!')
    
#--------------------------------------------------------------------------------------------------------------------------------------------------
    
    #ESTRAGGO DAL FILE L'INTERVALLO DI ANNI SPECIFICATO 
    #creo un'unica lista di liste contenente ogni anno compreso nell'intervallo
    anni_inclusi = []

    while first_year <= last_year:
        anno = []
        try:
            while indice_first_year<len(time_series) and first_year in time_series[indice_first_year][0]:
                anno.append(time_series[indice_first_year][1])
                #incremento se indice_first_year+1 != len(time_series)
                indice_first_year+=1
                

            #aggiungo la lista dell'anno n-esimo alla lista generale
            anni_inclusi.append(anno)
            #aggiorno first_year
            dati = time_series[indice_first_year][0].split('-')
            #esempio di come è dati a questo punto: ['1949', 112] 
            first_year = dati[0]
        except:
            #sono nella condizione in cui last_year == all'ultimo anno presente nel file e indice_first_year==len(time_series)
            first_year = str(int(last_year)+1)    

    #esempio di come è anni_inclusi a questo punto:
    # [ [112, 118, 129..], [115, 126, 141..], [145, 150, 178..] ..] 

#--------------------------------------------------------------------------------------------------------------------------------------------------

    #CALCOLO DELLA VARIAZIONE MEDIA DEI passeggeri

    #creo una lista delle differenze medie per i mesi
    diff_media_mesi = [0] * 12
    #per ogni n_dati_mese

    for mese in range(0, 12):
        #somma_tot corrisponde alla somma di tutte le differenze tra i vari anni per il mese n-esimo
        somma_tot=0
        #n_dati_mese corrisponde al numero totale di anni che hanno un dato valido per il mese n-esimo
        n_dati_mese=0
        for anno in range(0, len(anni_inclusi)-1):
            dato_anno = anni_inclusi[anno][mese]
            dato_anno_succ = anni_inclusi[anno+1][mese]
            if dato_anno>0 and dato_anno_succ>0:
                somma_tot += dato_anno_succ-dato_anno
                
                n_dati_mese+=1
            elif dato_anno>0 and dato_anno_succ==0:
                while anno<len(anni_inclusi)-1 and dato_anno_succ==0:
                    anno+=1
                    dato_anno_succ = anni_inclusi[anno][mese]

                if dato_anno_succ>0:
                    somma_tot += dato_anno_succ-dato_anno  
                    n_dati_mese+=1  
        
        if n_dati_mese>0:
            diff_media_mesi[mese] = round(somma_tot/n_dati_mese, 2)

    return diff_media_mesi    

#--------------------------------------------------------------------------------------------------------------------------------------------------

class CSVTimeSeriesFile(CSVFile):
    def __init__(self, name):
        super().__init__(name)

    def get_data(self):
        return super().get_data()
                    
#--------------------------------------------------------------------------------------------------------------------------------------------------

time_series_file = CSVTimeSeriesFile()

time_series = time_series_file.get_data(name='data.csv')

print(compute_avg_monthly_difference(time_series, '1949', '1950'))
