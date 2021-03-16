#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h> 

#define SIZE_ARR 100
#define TAM 1024
#define DIR_A 1
#define DIR_B 2
void read_command(char cmd[], char *par[])
{
    char line[TAM];
    
    int count = 0, i = 0, j = 0;
    char *array[100], *pch;
	for(j = 0; j < 100; j++) { array[j] = NULL; }
	for(j = 0; j < TAM; j++) { line[j] = (char)' '; }
	
    //Leer una línea
    for(;;) {
        int c = fgetc(stdin);
        line[count++] = (char) c;     
        if (c == '\n') { line[count] = (char)' '; break; }    
    }
    
    if (count == 1) { printf("Return por count 1\n"); return; }
    pch = strtok(line, " \n");
	
    //Análisis de la línea por palabras
    while (pch != NULL) {
        array[i++] = strdup(pch);
        pch = strtok(NULL, " \n");
    }
    // Command
    strcpy(cmd, array[0]);
    printf("cmd 0 -> %s\n", cmd);
    
    // Parameters
    
    for(j = 1; j < i; j++)
    {
		
		par[j-1] = array[j];
		printf("par %d -> %s|\n", j-1, par[j-1]);
	}
	
	par[j-1] = NULL;
	printf("par %d -> %s|\n", j-1, par[j-1]);
	
	
	free(pch);
}

int main()
{
	int test = 0, actDir = 1;// pointDir = 0;
	//char *dir[2] = {"/home/ignacioperez/PRUEBAS/Shell/DA/", "/home/ignacioperez/PRUEBAS/Shell/DB/"};
	char *help[] = {"exit", "a:", "b:", "help" };
	char *cmd, command[SIZE_ARR], *parameters[20];
	
	while(1) 
	{
		if(actDir == DIR_A) { printf("a:> ");}
		else if(actDir == DIR_B) {printf("b:> ");}
		
        if(fork() != 0) 
        { 
			wait(NULL);
        }
        else 
        {
			read_command(command, parameters);
			
			printf("comando -> %s|\n", command);
			if (strcmp(command, help[0]) == 0) 
			{ 
				printf("Estoy fuera\n"); 
				kill(getppid(), 9); 
				exit(0);
			}
			else if(strcmp(command, help[DIR_A]) == 0)
			{
				printf("DA\n");
				actDir = DIR_A;
			}
			else if(strcmp(command, help[DIR_B]) == 0)
			{
				printf("DB\n");
				actDir = DIR_B;
			}
			if (strcmp(command, help[3]) == 0)
			{ printf("\nComandos de la shell\n---------------------------\nCOPY     Copia el fichero de origen en el destino\nDIR      Muestra los ficheros de una unidad\nERA      Borra el fichero o grupo de ficheros\nEXIT     Cierra la shell\nREN      Mueve el fichero origen al destino\nRUN      Lanza un ejecutable en LINUX\nTYPE     Muestra el contenido de un fichero en modo texto\nHELP     Muestra un listado de comandos disponibles\n\n");}
		
			cmd = (char *)malloc(sizeof(char)*(sizeof(command)+4));
			strcpy(cmd, "/bin/");
			strcat(cmd, command);
	
			printf("%s", cmd);
			for(test = 0; parameters[test] != NULL; test++) {printf(" %s", parameters[test]);}
			printf("\n");
			
			exit(0);
        }
        
	}
	
            
	return 0;
}



















/*
int main()
{
    char *cmd, command[SIZE_ARR], *parameters[20];

	//char *envp[] = { (char *) "PATH=/bin", 0 };
	while (1) 
	{
		
		read_command(command, parameters);
        if(fork() != 0) 
        { 
			wait(NULL);
        }
        else {
			
            // execve(cmd, parameters, envp);

        }
        if (strcmp(command, "exit") == 0)
            break;
    }
    return 0;
}
*/
