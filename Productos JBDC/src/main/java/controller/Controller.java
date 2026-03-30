package controller;

import dto.PerfilesDTO;
import dto.UsersDTO;
import model.Perfiles;
import model.Users;

import java.sql.SQLException;
import java.util.stream.Stream;

public class Controller {
    private PerfilesDTO perfilesDTO;
    private UsersDTO usersDTO;

    public Controller(){
        this.perfilesDTO = new PerfilesDTO();
        this.usersDTO = new UsersDTO();
    }

    public void registrarPerfil(Perfiles perfiles){
        System.out.println("\nVamos a registrar un perfil");
        try {
            perfilesDTO.addPerfil(perfiles);
        } catch (SQLException e) {
            System.out.println("Error en el registro " + e.getMessage());
        }
    }

    public void registro(Users users){
        try {
            usersDTO.registro(users);
        } catch (SQLException e) {
            System.out.println("Error en el login del User " + e.getMessage());
        }
    }

}
