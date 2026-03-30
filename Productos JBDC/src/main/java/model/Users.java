package model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class Users {

    private int id;
    private String nombre;
    private String apellido;
    private String correo;
    private String pass;
    private int id_perfil;

    public Users(String nombre, String apellido, String correo, String pass, int id_perfil) {
        this.nombre = nombre;
        this.apellido = apellido;
        this.correo = correo;
        this.pass = pass;
        this.id_perfil = id_perfil;
    }
}
