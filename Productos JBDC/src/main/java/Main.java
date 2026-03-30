import dto.UsersDTO;
import model.Users;
import paneles.Admin;
import paneles.Cliente;

import java.io.IOException;
import java.sql.SQLException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        UsersDTO usersDTO = new UsersDTO();
        Users users;

        System.out.println("Servicio de compra");
        Scanner scanner = new Scanner(System.in);
        int opcion;

        do {
            System.out.println("\n1. Sacar Perfiles disponibles");
            System.out.println("2. Login User");
            System.out.println("3. Salir");
            opcion = scanner.nextInt();
            scanner.nextLine();
            switch (opcion) {
                case 1 -> {
                    try {
                        usersDTO.sacarPerfiles();
                    } catch (SQLException e) {
                        System.out.println("Error al sacar los perfiles disponibles" + e.getMessage());
                    }
                }
                case 2 -> {
                    try {
                        System.out.println("\n\tRegistro");
                        System.out.println("Introduzca nombre");
                        String nombre = scanner.nextLine();
                        System.out.println("Introduzca apellido");
                        String apellido = scanner.nextLine();
                        System.out.println("Introduzca correo");
                        String correo = scanner.nextLine();
                        System.out.println("Introduzca contraseña");
                        String pass = scanner.nextLine();
                        System.out.println("Introduzca id perfil");
                        int id_perfil = scanner.nextInt();
                        scanner.nextLine();

                        users = new Users(nombre, apellido, correo, pass, id_perfil);
                        usersDTO.registro(users);
                        System.out.println("Usuario esta guardado correctamente");

                        if (id_perfil == 1) {
                            usersDTO.borrarUsuario(users.getId());
                            System.out.println("Entrando al Admin panel");
                            Admin admin = new Admin();
                            admin.adminPanel();

                        } else if (id_perfil == 2) {
                            Cliente cliente = new Cliente(users);
                            cliente.menuCliente();
                        } else {
                            System.out.println("No perfil con ese id");
                        }
                    } catch (SQLException e) {
                        System.out.println("Error en el login de user");
                    }

                }
                case 3 -> {
                    System.out.println("Saliendo");

                }
                default -> {
                    System.out.println("Opcion no valida");
                }

            }
        } while (opcion!=3);

    }
}
