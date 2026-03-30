package dto;

import database.DBConnector;
import model.Perfiles;
import model.Users;
import utils.SchemDB;

import java.awt.dnd.DnDConstants;
import java.sql.*;

public class UsersDTO {
    private Connection connection;
    private Statement statement;
    private PreparedStatement preparedStatement;
    private ResultSet resultSet;

    private int nuevoID() throws SQLException {
        connection = DBConnector.getConnection();

        String query = String.format("SELECT MAX(id) FROM %s",SchemDB.TAB_USER);
        statement = connection.createStatement();
        resultSet = statement.executeQuery(query);

        int nextID=1;
        if (resultSet.next()){
            nextID = resultSet.getInt(1)+1;
        }

        return nextID;
    }

    public int registro(Users users) throws SQLException {
        connection = DBConnector.getConnection();

        int idNuevo = nuevoID();
        users.setId(idNuevo);

        String query = String.format("INSERT INTO %s (%s,%s,%s,%s,%s,%s)" +
                "VALUES (?,?,?,?,?,?)",
                SchemDB.TAB_USER,
                SchemDB.COL_ID, SchemDB.COL_NAME, SchemDB.COL_SURNAME,
                SchemDB.COL_MAIL, SchemDB.COL_PASSWORD, SchemDB.COL_ID_PERFIL);

        preparedStatement = connection.prepareStatement(query);
        preparedStatement.setInt(1, users.getId());
        preparedStatement.setString(2, users.getNombre());
        preparedStatement.setString(3, users.getApellido());
        preparedStatement.setString(4, users.getCorreo());
        preparedStatement.setString(5, users.getPass());
        preparedStatement.setInt(6, users.getId_perfil());

        System.out.println("Registrado nuevo user " + users.getNombre());
        int resultado = preparedStatement.executeUpdate();
        preparedStatement.close();
        return resultado;
    }
    public void borrarUsuario(int idUsuario) throws SQLException {
        connection = DBConnector.getConnection();
        String query = String.format("DELETE FROM %s WHERE %s = ?",
                SchemDB.TAB_USER, SchemDB.COL_ID);

        preparedStatement = connection.prepareStatement(query);
        preparedStatement.setInt(1, idUsuario);
        preparedStatement.executeUpdate();
        preparedStatement.close();
    }

    public void sacarPerfiles() throws SQLException {
        connection = DBConnector.getConnection();

        String query = String.format("SELECT * FROM %s ", SchemDB.TAB_PERFIL);

        statement = connection.createStatement();
        resultSet = statement.executeQuery(query);

        while (resultSet.next()){
            int id = resultSet.getInt("id");
            String nombre = resultSet.getString("nombre");
            System.out.println("ID -> "+id +", Role -> " +nombre);
        }
    }


    public void sacarProductos() throws SQLException {
        connection = DBConnector.getConnection();

        String query = String.format("SELECT * FROM %s", SchemDB.TAB_PRODUCT);

        statement = connection.createStatement();
        resultSet = statement.executeQuery(query);

        System.out.println();
        while (resultSet.next()){
            int id = resultSet.getInt("id");
            String nombre = resultSet.getString("nombre");
            int precio = resultSet.getInt("precio");
            String descripcion = resultSet.getString("descripcion");
            System.out.printf("\n\nID-> %d, \nNombre-> %s, \nPrecio-> %d, \nDescripcion-> %s",
                    id,nombre,precio,descripcion);

        }
    }

    public int insertarCarito(int idUser, int idProducto) throws SQLException {
        connection = DBConnector.getConnection();

        String query = String.format("INSERT INTO %s (%s,%s) VALUES (?,?)",
                SchemDB.TAB_CART,
                SchemDB.COL_ID_USER, SchemDB.COL_ID_PRODUCT);

        preparedStatement = connection.prepareStatement(query);
        preparedStatement.setInt(1, idUser);
        preparedStatement.setInt(2, idProducto);

        System.out.println("Producto aniadido al carito");
        return preparedStatement.executeUpdate();
    }

    public void mostrarCarito(int idUser) throws SQLException {
        connection = DBConnector.getConnection();

        String query = String.format("SELECT p.* FROM %s c JOIN %s p ON c.%s = p.%s WHERE c.%s = ?",
                SchemDB.TAB_CART,
                SchemDB.TAB_PRODUCT, SchemDB.COL_ID_PRODUCT, SchemDB.COL_ID, SchemDB.COL_ID_USER);

        preparedStatement = connection.prepareStatement(query);
        preparedStatement.setInt(1, idUser);
        resultSet = preparedStatement.executeQuery();

        System.out.println("\tProductos en carito");
        while (resultSet.next()){
            String nombre = resultSet.getString("nombre");
            int precio = resultSet.getInt("precio");
            System.out.printf("\nNombre del producto -> %s, Precio -> %d euros",nombre,precio);
        }
    }

    public int modificarPass(int idUser, String pass) throws SQLException {
        connection = DBConnector.getConnection();

        String query = String.format("UPDATE %s SET %s = ? WHERE %s = ?",
                SchemDB.TAB_USER,
                SchemDB.COL_PASSWORD, SchemDB.COL_ID);

        preparedStatement = connection.prepareStatement(query);
        preparedStatement.setString(1, pass);
        preparedStatement.setInt(2, idUser);

        System.out.println("Password cambiado");
        return preparedStatement.executeUpdate();
    }

    public void totalCompra(int idUsuario) throws SQLException {
        connection = DBConnector.getConnection();

        String query = String.format("SELECT p.%s, p.%s FROM %s c JOIN %s p ON c.%s = p.%s WHERE c.%s = ?",
                SchemDB.COL_NAME, SchemDB.COL_PRICE, SchemDB.TAB_CART, SchemDB.TAB_PRODUCT,
                SchemDB.COL_ID_PRODUCT, SchemDB.COL_ID, SchemDB.COL_ID_USER);

        preparedStatement = connection.prepareStatement(query);
        preparedStatement.setInt(1, idUsuario);
        resultSet = preparedStatement.executeQuery();

        double total = 0;

        while (resultSet.next()) {
            String nombre = resultSet.getString(SchemDB.COL_NAME);
            double precio = resultSet.getDouble(SchemDB.COL_PRICE);
            total += precio;
            System.out.printf("- %s: %.2f€\n", nombre, precio);
        }

        System.out.printf("\nTotal para pagar: %.2f euros\n", total);
    }

    public void verDatos(int idUser) throws SQLException {
        connection = DBConnector.getConnection();

        String consulta = String.format("SELECT * FROM %s WHERE %s = ?",
                SchemDB.TAB_USER,
                SchemDB.COL_ID);

        preparedStatement = connection.prepareStatement(consulta);
        preparedStatement.setInt(1, idUser);

        resultSet = preparedStatement.executeQuery();

        System.out.println("\n\tTUS DATOS PERSONALES");
        if (resultSet.next()) {
            int id = resultSet.getInt(SchemDB.COL_ID);
            String nombre = resultSet.getString(SchemDB.COL_NAME);
            String apellido = resultSet.getString(SchemDB.COL_SURNAME);
            String correo = resultSet.getString(SchemDB.COL_MAIL);
            String pass = resultSet.getString(SchemDB.COL_PASSWORD);
            int id_perfil = resultSet.getInt(SchemDB.COL_ID_PERFIL);

            System.out.printf("ID-> %d, Nombre-> %s, Apellido-> %s, Correo-> %s, Pass-> %s, ID de perfil-> %d",
                    id,nombre,apellido,correo,pass,id_perfil);

        } else {
            System.out.println("No hay datos de ese usuario");
        }
    }

    public void vaciarTablas() throws SQLException {
        connection = DBConnector.getConnection();

        String queryCarito = String.format("DELETE FROM %s", SchemDB.TAB_CART);
        String queryProductos = String.format("DELETE FROM %s", SchemDB.TAB_PRODUCT);

        statement = connection.createStatement();
        statement.executeUpdate(queryCarito);
        statement.executeUpdate(queryProductos);

        System.out.println("Tablas vaciadas correctamente (Carito y luego Productos)");
    }

}
