package controller;

import com.google.gson.Gson;
import dto.PerfilesDTO;
import dto.ProductoDTO;
import model.Productos;
import org.ietf.jgss.GSSContext;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.sql.SQLException;

public class APIController {
    private ProductoDTO productoDTO;
    private PerfilesDTO perfilesDTO;

    private String url = "https://dummyjson.com/products";
    private HttpClient client;
    private HttpRequest request;
    private HttpResponse<String> response;

    public APIController(){
        this.productoDTO = new ProductoDTO();
        this.perfilesDTO = new PerfilesDTO();
    }

    public void getProductos(){
        try {
            client = HttpClient.newHttpClient();
            request = HttpRequest.newBuilder().GET().uri(URI.create(url)).build();
            if (productoDTO.isVacia()){
                response = client.send(request, HttpResponse.BodyHandlers.ofString());
                String productosSTR = response.body();
                JSONObject productosJSON = new JSONObject(productosSTR);
                JSONArray productsArray = productosJSON.getJSONArray("products");
                for (int i = 0; i < productsArray.length(); i++) {
                    JSONObject jsonObject = productsArray.getJSONObject(i);

                    Productos productos = new Productos(
                            jsonObject.getInt("id"),
                            jsonObject.getString("title"),
                            jsonObject.getInt("price"),
                            jsonObject.getString("description")
                    );
                    productoDTO.addProducto(productos);
                }
                System.out.println("Productos aniadidos correctamente");
            } else {
                System.out.println("Tabla de productos ya tiene datos");
            }
        } catch (Exception e) {
            System.out.println("Error en la importacion de datos");
        }

    }
}
