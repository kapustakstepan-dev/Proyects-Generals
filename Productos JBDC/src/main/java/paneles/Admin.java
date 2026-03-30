package paneles;

import controller.APIController;
import dto.UsersDTO;
import model.Users;
import utils.SchemDB;

import java.sql.SQLException;
import java.util.Scanner;

public class Admin {
    private UsersDTO usersDTO = new UsersDTO();
    private APIController apiController = new APIController();
    private Scanner scanner = new Scanner(System.in);

    public void adminPanel(){
        int opcion;
        do {
            System.out.println("\n\tAdmin Panel");
            System.out.println("1. Crear nuevo Admin");
            System.out.println("2. Importar productos desde la API");
            System.out.println("3. Vaciar tablas Carito y Productos");
            System.out.println("4. Salir");
            System.out.println("Que eliges?");
            opcion = scanner.nextInt();
            scanner.nextLine();
            try {
                switch (opcion){
                    case 1 ->{
                        System.out.print("Nombre: ");
                        String nombre = scanner.nextLine();
                        System.out.print("Apellido: ");
                        String apellido = scanner.nextLine();
                        System.out.print("Correo: ");
                        String correo = scanner.nextLine();
                        System.out.print("Pass: ");
                        String pass = scanner.nextLine();

                        Users adminNuevo = new Users(nombre,apellido,correo,pass,1);
                        usersDTO.registro(adminNuevo);
                        System.out.println("Admin aniadido");
                    }
                    case 2 ->{
                        apiController.getProductos();
                    }
                    case 3 ->{
                        usersDTO.vaciarTablas();
                    }
                    case 4 ->{
                        System.out.println("Saliendo ...");
                    }
                    default -> {
                        System.out.println("Opcion no valida");
                    }
                }

            } catch (SQLException e){
                System.out.println("Error en Base de Datos " + e.getMessage());
            }

        } while (opcion !=4);
    }

}
