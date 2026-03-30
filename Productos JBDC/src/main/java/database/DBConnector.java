package database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnector {
    private static Connection connection;

    public static Connection getConnection(){
        if (connection==null){
            createConnection();
        }
        return connection;
    }

    private static void createConnection(){
        String user = "root";
        String pass = "foximiliano";
        String host = "127.0.0.1";
        String dbname = "compras_ces";
        String urlConnection = String.format("jdbc:mysql://%s/%s",host, dbname);
        try {
            connection = DriverManager.getConnection(urlConnection, user, pass);
        } catch (SQLException e) {
            System.out.println("Error en SQL");
            System.out.println(e.getMessage());
        }
    }

    private static void closeConnection(){
        if (connection!=null){
            try {
                connection.close();
            } catch (SQLException e) {
                System.out.println("Error al cerar Bases de Datos");
            }
        }
    }
}
