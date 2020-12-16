/*
standard library of Gabriele Ferrero
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

int ctoi(char *carattere){      // funzione per convertire una stringa contenente un numero intero

    int numero_finale=0;
    int numero_volte_carattere_meno_inserito=0;
    int numero_cifre_numero=0;
    int i=0;

    for(numero_cifre_numero=0; (*(carattere+numero_cifre_numero))!='\0'; numero_cifre_numero++){}

    for(i=0; (((*(carattere+i))=='-') || ((*(carattere+i))=='0') || ((*(carattere+i))=='1') || ((*(carattere+i))=='2') || ((*(carattere+i))=='3') || ((*(carattere+i))=='4') || ((*(carattere+i))=='5') || ((*(carattere+i))=='6') || ((*(carattere+i))=='7') || ((*(carattere+i))=='8') || ((*(carattere+i))=='9')) && ((*(carattere+i))!='\0'); i++){

        numero_finale=numero_finale*10;

        switch (*(carattere+i)){
        case '-':
        numero_volte_carattere_meno_inserito++;
        break;
        case '0':
        numero_finale=numero_finale+0;
        break;
        case '1':
        numero_finale=numero_finale+1;
        break;
        case '2':
        numero_finale=numero_finale+2;
        break;
        case '3':
        numero_finale=numero_finale+3;
        break;
        case '4':
        numero_finale=numero_finale+4;
        break;
        case '5':
        numero_finale=numero_finale+5;
        break;
        case '6':
        numero_finale=numero_finale+6;
        break;
        case '7':
        numero_finale=numero_finale+7;
        break;
        case '8':
        numero_finale=numero_finale+8;
        break;
        case '9':
        numero_finale=numero_finale+9;
        break;
        default:
        break;
        }
    }

    if(numero_volte_carattere_meno_inserito==1){
        return numero_finale*(-1);
    }else if(numero_volte_carattere_meno_inserito==0){
        return numero_finale;
    }else{
        
    }

}



#define max_caratteri_per_stringa 3000

void scanfInt(char stringa[max_caratteri_per_stringa], int *numero){      //funzione per il la stampa di una stringa e l'acquisizione di un int
    printf("%s", stringa);
    scanf("%d", numero);
}

void scanfChar(char stringa[max_caratteri_per_stringa], char *carattere){      //funzione per il la stampa di una stringa e l'acquisizione di un char
    printf("%s", stringa);
    scanf("%c", carattere);
}

void scanfFloat(char stringa[max_caratteri_per_stringa], float *numero_con_virgola){      //funzione per il la stampa di una stringa e l'acquisizione di un float
    printf("%s", stringa);
    scanf("%f", numero_con_virgola);
}

void scanfString(char stringa[max_caratteri_per_stringa], char *string){      //funzione per il la stampa di una stringa e l'acquisizione di una stringa
    char ch;
    int i=0;
    printf("%s", stringa);
    for(i=0; (ch=getchar())!='\n' ; i++){
        (*(string+i))=ch;
    }
    (*(string+i))='\0';
}








/*

#define numero_parametri_int 2
#define numero_parametri_char 2
#define numero_parametri_float 2
#define numero_parametri_caratteri_speciali 1


bool controlloNumero(char *dato, char stringa[max_caratteri_per_stringa]){   // funzione in cui si è obbligati a mettere prima e sempre la lettera i (intero) e poi tutto il resto

    bool verifica=true;
    int numero_cifre_per_int=0;
    int numero_int=0;

    for(numero_cifre_per_int=0; (*(dato+numero_cifre_per_int))!=' '; numero_cifre_per_int++)  //for per scoprire da quante cifre è composto un numero

    numero_int=ctoi(dato, numero_cifre_per_int);

    for(int i=0; ((*(stringa+i))!='\0') && (i<max_caratteri_per_stringa); i++){

        switch (*(stringa+i)){
        case 'i':   //caso intero

        break;

        case 'f':
        break;

        case 'c':
        if((dato>='a' && dato<='z') || (dato>='A' && dato<='Z')){

        }else{
            return false;
        }
        
        break;


        case '+':   //caso positivo
        if(numero>0){
        }else{
            return false;
        }
        break;


        case '-':   //caso negativo
        if(numero>0){
        }else{
            return false;
        }
        break;


        case '=':
        break;
        case 'P':
        break;
        case 'D':
        break;
        case 'p':
        break;


        case 'M':
        if(dato>='A' && dato<='Z'){
        }else{
            return false;
        }
        break;


        case 'm':
        if(dato>='a' && dato<='z'){
        }else{
            return false;
        }
        break;


        default:
        return false;
        break;
    }
    }

    return verifica;
    
}

bool controlloChar(char carattere, char stringa[]){}

*/
