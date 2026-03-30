package dto;

import database.DBConnector;
import model.Productos;
import utils.SchemDB;

import java.sql.*;

public class ProductoDTO {

    private Connection connection;
    private Statement statement;
    private PreparedStatement preparedStatement;
    private ResultSet resultSet;

    public int addProducto(Productos productos) throws SQLException {
        connection = DBConnector.getConnection();

        String query = String.format("INSERT INTO %s (%s,%s,%s,%s)" +
                "VALUES (?,?,?,?)",
                SchemDB.TAB_PRODUCT,
                SchemDB.COL_ID, SchemDB.COL_NAME, SchemDB.COL_PRICE, SchemDB.COL_DESCRIPTION);

        preparedStatement = connection.prepareStatement(query);
        preparedStatement.setInt(1, productos.getId());
        preparedStatement.setString(2,productos.getNombre());
        preparedStatement.setInt(3, productos.getPrecio());
        preparedStatement.setString(4, productos.getDescripcion());

        return preparedStatement.executeUpdate();
    }

    public boolean isVacia() throws SQLException {
        connection = DBConnector.getConnection();

        String query = String.format("SELECT COUNT(*) FROM %s",SchemDB.TAB_PRODUCT);
        statement = connection.createStatement();
        resultSet = statement.executeQuery(query);

        if (resultSet.next()){
            int cantidad = resultSet.getInt(1);
            return cantidad == 0;

        }
        return false;
    }


}
