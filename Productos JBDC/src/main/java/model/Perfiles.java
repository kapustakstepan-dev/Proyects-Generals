package model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class Perfiles {
    private static int contadorID;

    private int id;
    private String nombre;

    public Perfiles(String nombre) {
        this.id = ++contadorID;
        this.nombre = nombre;
    }
}
