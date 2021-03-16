; This is a basic template file for writing 48K Spectrum code.

AppFilename             equ "NewFile"                   ; What we're called (for file generation)

AppFirst                equ $8000                       ; First byte of code (uncontended memory)

                        zeusemulate "48K","ULA+"        ; Set the model and enable ULA+


; Start planting code here. (When generating a tape file we start saving from here)

                        org AppFirst                    ; Start of application


AppEntry               call cargarcoordenadasantiguas
                       call Teclado                  ;      call fillscreen

                       call copiarCarretera
                       call ActualizarCarretera
                       call ComprobarChoque
                       call limpiarcarretera
                       call PintarCarretera

                        call PintarCoche
                      ;  call limpiarmierda
                        call delay;
                        call Niveles;

                        jp AppEntry

cargarcoordenadasantiguas   ld a,(coordenadaX)
                        ld (coordenadaXold),a
                        ld a,(coordenadaY)
                        ld (coordenadaYold),a
                        ret


ComprobarChoque         ld a,(X1)
                        ld d, a
                        ld a,(coordenadaX)
                        cp d
                        jp z,fin;
                        add a,-8         ;Como la separacion es de 8 restamos 8 al coche para que coja el otro muro tambien
                        cp d
                        jp z,fin;
                        ret

limpiarmierda           ld bc, cochevacio
                        ld ix, (cocheantiguo)
                        ld ix , bc
                        ld a, (coordenadaYold)
                        ld d, a
                        ld a, (coordenadaXold)
                        ld c, a
                        call TC
                        ret


PintarCoche             ld de, 5AA0h
                        ld a, (coordenadaXold)
                        add de,a
                        ld hl, colorNiveles
                        ld a,(nivelActual)
                        add hl,a
                        ld a, (hl)
                        ld (de),a

                        ld de, 5AA0h
                        ld a, (coordenadaX)
                        add de,a
                        ld hl, colorCoche
                        ld a,(nivelActual)
                        add hl,a
                        ld a, (hl)
                        ld (de),a

                        ld ix, coche
                        ld a, (coordenadaY)
                        ld d, a
                        ld a, (coordenadaX)
                        ld c, a
                       ; ld ix, cochevacio
                        ld (cocheantiguo), ix


                        call TC
                        ret

PintarCarretera         ld iy, datosCarretera
                        ld b, 22
                        ld d, 0
PintarCarreteraBucle    ld c, (iy)
                        ld ix, completo
                        ld e, b
                        call TC
                        ld a, c
                        add a,8//se añade 8, porque 8 son los espacios que hay entre las carreteras
                        ld c, a
                        ld ix, completo
                        call TC
                        ld b, e
                        ld a , d
                        add a, 8
                        ld d, a
                        inc iy
                        djnz PintarCarreteraBucle
                        ret

Niveles                 ld a, (puntuacion)
                        inc a
                        cp 100
                        jp z cambiarNivel
                        ld (puntuacion),a
                        ret

cambiarNivel            ld a,0
                        ld (puntuacion),a
                        ld hl, 5800h
                        ld ix,colorNiveles
                        ld a, (nivelActual)
                        inc a
                        ld (nivelActual),a
                        ld b,a
incremento2             inc ix
                        djnz incremento2
                        ld b,255
                        call bucleNiveles
                        ld b,255
                        call bucleNiveles
                        ld b,255
                        call bucleNiveles
                        ld b,4
                        call bucleNiveles
                        ret

bucleNiveles            ld a,(ix)
                        ld (hl),a
                        inc hl
                        djnz bucleNiveles
                        ret


Teclado                 ld bc,0DFFEh                    ;       Cambiamos la primera parte de FE por FF
                        ;ei
                        in a,(c)                        ;
                        rra                             ; b0 'P'
                        push af                         ;
                        call nc,mvcaracter_right        ;
                        pop af                          ;
                        rra                             ; b1 'O'
                                        ;rra                             ; b1 'Z'
                                        ;push af                         ;
                                        ;call nc,mvcaracter_right ; call nc,mvcaracter_left         ;
                                        ;pop af                          ;
                        rra                             ; b2 'I'
                        push af                         ;
                        call nc,mvcaracter_left         ;
                        pop af                          ;
                        rra                             ;b3  'U'
                        rra                             ;b4  'Y'

                      ;
                       ; di   //Desactivar interrucpciones teclado
                        ret                             ;


mvcaracter_left         nop                             ;
                        ld hl,coordenadaX                     ;
                        ld a,(hl)                       ;
                        ;cp LX1                            ; ¿Estamos en la izquierda?
                     ;   ret c                           ;
                        dec (hl)
                        ;Como el coche se ha movido la posicion x cambia y tendremos que (limpiarla)
                        call limpiarmierda
                        ret                             ;

; Mover jugador a la derecha.
mvcaracter_right        nop                             ;
                        ld hl,coordenadaX                     ;
                        ld a,(hl)                       ;
                        ;cp LX2                           ; ¿Estamos en el borde derecho?
                      ;  ret nc                          ;
                        inc (hl)                       ;
                        ;Como el coche se ha movido la posicion x cambia y tendremos que (limpiarla)
                        call limpiarmierda
                        ret

delay                   call cargardificultad;
                                        ;ld b length of delay.
delay0                  halt                            ; wait for an interrupt.
                        djnz delay0                     ; loop.
                        ret

cargardificultad        ld a, (nivelActual)
                        ld b, 8
                        cp a, 0
                        ret z
                        cp a, 1
                        ld b, 7
                        ret z
                        cp a, 2
                        ld b, 6
                        ret z
                        cp a, 3
                        ld b, 5
                        ret z
                        cp a, 4
                        ld b, 4
                        ret z
                        cp a, 5
                        ld b, 3
                        ret z
                        cp a, 6
                        ld b, 2
                        ret z
                        cp a, 7
                        ld b, 1
                        ret z
                        ld b,0
                        ret



copiarCarretera           ld b, 22
                        ld hl, datosCarretera+21
bucle                   ld a,(hl);Siempre parentesis no {}
                        push af
                        dec hl       ;MD Incrmementa hl
                        djnz bucle     ;Ira hacia el bucle

                        ld b,22
                        ld hl, CarreteraAntigua
bucle2                  pop af
                        ld (hl),a
                        inc hl
                        djnz bucle2
                        ret


limpiarcarretera        ld iy, CarreteraAntigua
                       ; ld de, datosCarretera

                        ld b, 22
                        ld d, 0
limpiarcarreteraBucle   ld c, (iy)
                       ; ld a, (de)
                        cp c
                        ld ix, vacio
                        ld e, b
                        call TC
                        ; call nz, TC
                        ld a, c
                        add a,8//se añade 8, porque 8 son los espacion que hay entre las carreteras
                        ld c, a
                        ld ix, vacio
                        call TC
                       ; call nz, TC
                        ld b, e
                        ld a , d
                        add a, 8
                        ld d, a
                        inc iy
                        ;inc de
                        djnz limpiarcarreteraBucle
                        ret


ActualizarCarretera     ld b, 21
                        ld iy, datosCarretera +21
                        ld a, (datosCarretera +21) ; Esto es para poner en a la primera x de la carretera
                        ld (X1), a
                        ld a,r
                        and 1;
                        jp z, DesplazarDerecha
                        jp  DesplazarIzquierda
                        ret

DesplazarIzquierda      ld a, (iy)
                        cp 1
                        jp z, DesplazarCentro         ;ret z
                        dec iy
                        ld a , (iy)
                        inc iy
                        ld (iy), a
                      ;  ld a,5
                      ;  ld iy, a
                        dec iy
                        djnz DesplazarIzquierda

                        ld a, (iy)
                        add a, -1
                        ld (iy), a
                        ret

DesplazarDerecha         ld a, (iy)
                        cp 22 ; Es 23 porque es 31 y la distancia del primer muro a la que esta es de 28 por lo tanto 31-8
                          jp z, DesplazarCentro
                        dec iy
                        ld a , (iy)
                        inc iy
                        ld (iy), a
                      ;  ld a,5
                      ;  ld iy, a
                        dec iy
                        djnz DesplazarDerecha

                        ld a, (iy)
                        add a, 1
                        ld (iy), a
                        ret


DesplazarCentro         ld a , (iy)
                        dec iy
                        ld a , (iy)
                        inc iy
                        ld (iy), a
                      ;  ld a,5
                      ;  ld iy, a
                        dec iy
                        djnz DesplazarCentro
                        ret

;En c se envia la cord X
;En d se envia la cord Y

TC                      ld a, d ;Cambio el registro L
                        rla
                        rla
                        and 11100000b
                        ld l, a
                        ld a, c
                        and 00011111b
                        or l
                        ld l, a

                        ld a, 01000000b ;Cambio el registro L
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


;En HL se envia la direccion de comienzo
;En IX se envia el codigo hexadecimal del octeto
dibujar                 ld b,8

dibujarBucle            ld a, (ix)
                        ld (hl), a
                        add hl, 256
                        inc ix
                        djnz dibujarBucle
                        ret

;fin                     halt
 ;                       jp fin

coche                   defb 60,66,255,219,90,219,219,60
cochevacio              defb 0, 0, 0,  0,  0, 0, 0,0
vacio                   defs 8
completo                defb 255,255,255,255,255,255,255,255
datosCarretera          defb 6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6
CarreteraAntigua        defs 22
X1                      defb 3          ;Aqui va a estar la primera x que va a comprobar si te chocas
coordenadaX             defb 9
coordenadaY             defb 168
coordenadaXold          defb 0
coordenadaYold          defb 0
cocheantiguo            defs 8
direccionlimpiar        defb 0;
puntuacion              defb 0;
colorNiveles            defb 56,32,50,41,7,55,26,40
colorCoche              defb 58,34,50,42,2,50,26,45
nivelActual             defb 6;



fin                            halt;


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

