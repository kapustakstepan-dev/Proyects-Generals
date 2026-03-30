package paneles;

import dto.UsersDTO;
import model.Users;

import java.sql.SQLException;
import java.util.Scanner;

public class Cliente {

    private UsersDTO usersDTO = new UsersDTO();
    private Scanner scanner = new Scanner(System.in);
    private Users users;

    public Cliente(Users users) {
        this.users = users;
    }

    public void menuCliente(){
        int opcion;
        do {
            System.out.println();
            System.out.println("\n\tMenu Cliente");
            System.out.println("1. Ver sus datos");
            System.out.println("2. Modificar pass");
            System.out.println("3. Ver los productos");
            System.out.println("4. Seleccionar producto compra");
            System.out.println("5. Mostrar carrito");
            System.out.println("6. Ver total compra");
            System.out.println("7. Salir");
            System.out.println();
            System.out.println("Que eliges? ");
            opcion = scanner.nextInt();
            scanner.nextLine();
            try {
                switch (opcion) {
                    case 1 -> {
                        usersDTO.verDatos(users.getId());
                    }
                    case 2 -> {
                        System.out.println("Introduzca password nuevo -> ");
                        String pass = scanner.nextLine();
                        usersDTO.modificarPass(users.getId(), pass);
                    }
                    case 3 ->{
                        usersDTO.sacarProductos();
                    }
                    case 4 -> {
                        System.out.println("Introduzca id del producto para comprar ->");
                        int id = scanner.nextInt();
                        usersDTO.insertarCarito(users.getId(), id);
                    }
                    case 5 -> {
                        usersDTO.mostrarCarito(users.getId());
                    }
                    case 6 -> {
                        usersDTO.totalCompra(users.getId());
                    }
                    case 7 -> {
                        System.out.println("Saliendo ...");
                    }
                    default -> {
                        System.out.println("Opcion no valida");
                    }
                }
            } catch (SQLException e){
                System.out.println("Error en Base de Datos " + e.getMessage());
            }

        } while (opcion!=7);
    }


}
