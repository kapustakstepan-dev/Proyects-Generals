package dto;

import database.DBConnector;
import model.Perfiles;
import utils.SchemDB;

import java.sql.*;

public class PerfilesDTO {

    private Connection connection;
    private Statement statement;
    private PreparedStatement preparedStatement;
    private ResultSet resultSet;

    public int addPerfil(Perfiles perfiles) throws SQLException {
        connection = DBConnector.getConnection();

        String query = String.format("INSERT INTO %s (%s,%s)" +
                "VALUES (?,?)",
                SchemDB.TAB_PERFIL,
                SchemDB.COL_ID, SchemDB.COL_NAME);

        preparedStatement = connection.prepareStatement(query);
        preparedStatement.setInt(1, perfiles.getId());
        preparedStatement.setString(2, perfiles.getNombre());
        return preparedStatement.executeUpdate();
    }



}
