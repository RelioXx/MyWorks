; This is a basic template file for writing 48K Spectrum code.

AppFilename             equ "NewFile"                   ; What we're called (for file generation)

AppFirst                equ $8000                       ; First byte of code (uncontended memory)

                        zeusemulate "48K","ULA+"        ; Set the model and enable ULA+


; Start planting code here. (When generating a tape file we start saving from here)
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/                                                                                                                        /
/    C�DIGO CREADO POR:                                                                                                  /
/                                                                                                                        /
/     Alex Silvestre                                                                                                     /
/     �lvaro Puente                                                                                                      /
/     Jorge de Santiago                                                                                                  /
/                                                                                                                        /
/                                                                                                                        /
/    IDCD 1�  Pr�ctica 2:Proyecto de ensamblador          ESTRUCTURAS DE LOS ORDENADORES                                 /
/                                                                                                                        /
/                                                                                                                        /
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
*/
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                        org AppFirst                    ; Start of application

;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;BUCLE: --> SE REPETIR� TODO EL RATO HASTA QUE EL COCHE SE CHOQUE
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

AppEntry               call cargarcoordenadasantiguas

                       call Teclado

                       call copiarCarretera

                       call ActualizarNuevaCarretera
                       call ComprobarChoque;

                       call PintarCarretera

                        call PintarCoche


                        call delay;
                        call Niveles;

                        jp AppEntry


;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



cargarcoordenadasantiguas   ld a,(coordenadaX)
                        ld (coordenadaXold),a
                        ld a,(coordenadaY)
                        ld (coordenadaYold),a   ;Cargamos las coordenas antiguas para luego cuando limpiemos el coche.
                        ret


ComprobarChoque         ld a,(X1)     //X1 es el lugar donde esta el muro de abajo del todo
                        ld d, a
                        ld a,(coordenadaX)
                        cp d
                        jp z,fin;     ;Si se compara y z esta activado entonces se acabar� el juego porque el coche se habr� chocado
                        add a,-8         ;Como la separaci�n es de 8 restamos 8 al coche para que coja el otro muro tambi�n
                        cp d
                        jp z,fin;
                        ret

;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;PINTAR Y LIMPIAR
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

LimpiarCoche           ld bc, cochevacio          ;Cargamos una informacion vacia (0) que se pasar� para que no se ponga nada en la pantalla
                        ld ix, (cocheantiguo)
                        ld ix , bc
                        ld a, (coordenadaYold)
                        ld d, a
                        ld a, (coordenadaXold)
                        ld c, a
                        call TraducirCoords
                        ret


PintarCoche             ld de, 5AA0h
                        ld a, (coordenadaXold)
                        add de,a                   ;Cargamos en DE la posici�n de la antigua posici�n del coche
                        ld hl, colorNiveles
                        ld a,(nivelActual)
                        add hl,a
                        ld a, (hl)
                        ld (de),a                  ;Y pintamos del color del fondo en la posici�n antigua

                        ld de, 5AA0h
                        ld a, (coordenadaX)
                        add de,a                   ;Cargamos en DE la posici�n de la actual posici�n del coche
                        ld hl, colorCoche
                        ld a,(nivelActual)
                        add hl,a
                        ld a, (hl)
                        ld (de),a                  ;Y pintamos del color del coche en su posici�n

                        ld ix, coche
                        ld a, (coordenadaY)
                        ld d, a
                        ld a, (coordenadaX)
                        ld c, a
                        ld (cocheantiguo), ix

                        call TraducirCoords         ;Y luego pintamos el coche llamando a la rutina de coordenadas
                        ret

PintarCarretera         call limpiarcarretera
                        ld iy, CarreteraCoords
                        ld b, 22
                        ld d, 0
PintarCarreteraBucle    ld c, (iy)
                        ld ix, completo
                        ld e, b
                        call TraducirCoords
                        ld a, c
                        add a,8                     ;Se a�ade 8, porque 8 son los espacios que hay entre las carreteras
                        ld c, a
                        ld ix, completo
                        call TraducirCoords
                        ld b, e
                        ld a , d
                        add a, 8
                        ld d, a
                        inc iy
                        djnz PintarCarreteraBucle
                        ret

;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;CONTROL DE NIVELES
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Niveles                 ld a, (puntuacion)
                        inc a
                        cp 100                       ;La puntuaci�n es como un contador, cuando llega a 100 cambia de nivel, y vuelve a 0
                        jp z cambiarNivel
                        ld (puntuacion),a
                        ret

cambiarNivel            ld a,0
                        ld (puntuacion),a
                        ld hl, 5800h                 ;Desde la primera posici�n, pinto toda la pantalla
                        ld de,colorNiveles
                        ld a, (nivelActual)
                        inc a
                        ld (nivelActual),a
                        add de,a
                        ld b,255
                        call bucleNiveles
                        ld b,255
                        call bucleNiveles
                        ld b,255
                        call bucleNiveles
                        ld b,4
                        call bucleNiveles
                        ret

bucleNiveles            ld a,(de)
                        ld (hl),a
                        inc hl
                        djnz bucleNiveles
                        ret


;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;DETECCION DE CONTROL --> MOVIMIENTO DEL COCHE
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Teclado                 ld bc,0DFFEh                    ;       Cambiamos la primera parte de FE por FF
                        in a,(c)                        ;
                        rra                             ; b0 'P'
                        push af                         ;
                        call nc,mvcaracter_right        ;
                        pop af                          ;
                        rra                             ; b1 'O'
                        rra                             ; b2 'I'
                        push af                         ;
                        call nc,mvcaracter_left         ;
                        pop af                          ;
                        rra                             ;b3  'U'
                        rra                             ;b4  'Y'

                        ret                             ;

; Mover jugador a la izquierda.
mvcaracter_left         nop                             ;
                        ld hl,coordenadaX               ;
                        ld a,(hl)                       ;
                        dec (hl)                        ; se resta 1 en la posici�n X
                                      ;Como el coche se ha movido la posici�n x cambia y tendremos que (limpiarla)
                        call LimpiarCoche
                        ret                             ;

; Mover jugador a la derecha.
mvcaracter_right        nop                             ;
                        ld hl,coordenadaX               ;
                        ld a,(hl)                       ;
                        inc (hl)                        ; se suma 1 en la posici�n X
                        ;Como el coche se ha movido la posici�n x cambia y tendremos que (limpiarla)
                        call LimpiarCoche
                        ret


;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



delay                   call cargardificultad;

delay0                  halt                            ; espera a una interrupci�n
                        djnz delay0                     ; bucle
                        ret

cargardificultad        ld a, (nivelActual)     ;Aqui se cargara la dificultad, dependiendo del nivel se reducir�n los halts
                        ld b, 7
                        cp a, 0
                        ret z
                        cp a, 1
                        ld b, 6
                        ret z
                        cp a, 2
                        ld b, 5
                        ret z
                        cp a, 3
                        ld b, 4
                        ret z
                        cp a, 4
                        ld b, 3
                        ret z
                        cp a, 5
                        ld b, 2
                        ret z
                        ld b,1
                        ret



copiarCarretera           ld b, 22  ;Este es un m�todo para copiar la carretera y as� reducir el efecto flick para pasar
;las coordenadas mas rapido en el tiempo entre que se borra los antiguos muros y que se vuelven a pintar

                        ld hl, CarreteraCoords+21
bucle                   ld a,(hl)               ;Siempre parentesis no {}
                        push af
                        dec hl                  ;MD Incrmementa hl
                        djnz bucle              ;Ir� hacia el bucle

                        ld b,22
                        ld hl, CarreteraAntigua
bucle2                  pop af
                        ld (hl),a
                        inc hl
                        djnz bucle2
                        ret



;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;LIMPIAR CARRETERA
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


limpiarcarretera        ld iy, CarreteraAntigua

                        ld b, 22
                        ld d, 0
limpiarcarreteraBucle   ld c, (iy)
                        cp c
                        ld ix, vacio
                        ld e, b
                        call TraducirCoords
                        ld a, c
                        add a,8                 ;se a�ade 8, porque 8 son los espacios que hay entre las carreteras
                        ld c, a
                        ld ix, vacio
                        call TraducirCoords
                        ld b, e
                        ld a , d
                        add a, 8
                        ld d, a
                        inc iy
                        djnz limpiarcarreteraBucle

                        ret


;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;CONTROL DE CARRETERA
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


ActualizarNuevaCarretera     ld b, 21                   ;Lo grande que es de altura los muros de la carretera
                        ld iy, CarreteraCoords +21
                        ld a, (CarreteraCoords +21)     ;Esto es para poner en a la primera x de la carretera
                        ld (X1), a
                        ld a,r                          ;R es un registro que se actualiza de manera aleatoria
                        and 1;                          ;Para la flag z
                        jp z, MoverCarreteraDerecha     ;Dependiendo (de forma aleatoria) de la flag z se movera a la derecha o a la izquierda
                        jp  MoverCarreteraIzquierda  ;Si no es a la derecha sera a la izquierda
                        ret




;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;DIRECCION DE MOVIMIENTO DE CARRETERA
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


MoverCarreteraIzquierda      ld a, (iy)
                        cp 1
                        jp z, DesplazarCentro
                        dec iy
                        ld a , (iy)
                        inc iy
                        ld (iy), a
                        dec iy
                        djnz MoverCarreteraIzquierda

                        ld a, (iy)
                        add a, -1       ;Esto reducir� en 1 la cordenada x donde esta el muro, asi se mover� a la izquierda
                        ld (iy), a
                        ret

MoverCarreteraDerecha         ld a, (iy)
                        cp 22           ; Es 23 porque es 31 y la distancia del primer muro a la que esta es de 28 por lo tanto 31-8
                          jp z, DesplazarCentro
                        dec iy
                        ld a , (iy)
                        inc iy
                        ld (iy), a
                        dec iy
                        djnz MoverCarreteraDerecha

                        ld a, (iy)
                        add a, 1      ;Esto aumentara en 1 la cordenada x donde esta el muro, asi se mover� a la izquierda
                        ld (iy), a
                        ret


DesplazarCentro         ld a , (iy)
                        dec iy
                        ld a , (iy)
                        inc iy
                        ld (iy), a
                        dec iy
                        djnz DesplazarCentro
                        ret



;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;PASAR COORDENADAS A MEMORIA , C�DIGO EXTRA�DO DE -> http://www.breakintoprogram.co.uk/computers/zx-spectrum/screen-memory-layout
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

;La coordenada x se envia con el registro c  (Antes era b pero necesitamos b en la funcion anterior para el bucle
;La coordenada y se envia con el registro d
TraducirCoords          ld a, d
                        rla
                        rla
                        and 11100000b
                        ld l, a
                        ld a, c
                        and 00011111b
                        or l
                        ld l, a

                        ld a, 01000000b
                        ld h, a
                        ld a, d
                        and 00000111b
                        or h
                        ld h, a
                        ld a, d
                        and 11000000b
                        rra
                        rra
                        rra
                        or h
                        ld h,a

                        call dibujar
                        ret



;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;BUCLE DIBUJAR
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


dibujar                 ld b,8

dibujarBucle            ld a, (ix)
                        ld (hl), a
                        add hl, 256
                        inc ix
                        djnz dibujarBucle
                        ret

;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;DATOS DE MEMORIA (y variables)
;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



coche                   defb 60,66,255,219,90,219,219,60
cochevacio              defb 0, 0, 0,  0,  0, 0, 0,0
vacio                   defs 8
completo                defb 251,251,0,223,223,0,251,251
CarreteraCoords          defb 6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6
CarreteraAntigua        defs 22
X1                      defb 3          ;Aqu� va a estar la primera x que va a comprobar si te chocas
coordenadaX             defb 11
coordenadaY             defb 168
coordenadaXold          defb 0
coordenadaYold          defb 0
cocheantiguo            defs 8
direccionlimpiar        defb 0;
puntuacion              defb 0;
colorNiveles            defb 56,32,50,41,7,55,26,40        ;Color del fondo seg�n niveles
colorCoche              defb 58,34,50,42,2,50,26,45        ;Color del coche seg�n niveles
nivelActual             defb 0;



fin                            halt;

;---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
;FIN DEL CODIGO
;----------------------------------------------------------------------------------------------------------------------------------------------------------


; Stop planting code after this. (When generating a tape file we save bytes below here)
AppLast                 equ *-1                         ; The last used byte's address

; Generate some useful debugging commands

                        profile AppFirst,AppLast-AppFirst+1     ; Enable profiling for all the code

; Setup the emulation registers, so Zeus can emulate this code correctly

Zeus_PC                 equ AppEntry                            ; Tell the emulator where to start
Zeus_SP                 equ $FF40                               ; Tell the emulator where to put the stack

; These generate some output files

                        ; Generate a SZX file
                        output_szx AppFilename+".szx",$0000,AppEntry    ; The szx file

                        ; If we want a fancy loader we need to load a loading screen
;                        import_bin AppFilename+".scr",$4000            ; Load a loading screen

                        ; Now, also generate a tzx file using the loader
                        output_tzx AppFilename+".tzx",AppFilename,"",AppFirst,AppLast-AppFirst,1,AppEntry ; A tzx file using the loader
