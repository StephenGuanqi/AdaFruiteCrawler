package edu.cmu.guanqiy.adafruite;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Array;
import java.util.ArrayList;

public class Product {

    private String name;

    private String price;

    private String url;

    private String imageUrl;

    private String descripton;

    private String amountLeft;

    public void setAmountLeft(String amountLeft) {
        this.amountLeft = amountLeft;
    }

    public String getAmountLeft() {

        return amountLeft;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public void setDescripton(String descripton) {
        this.descripton = descripton;
    }

    public void setName(String name) {

        this.name = name;
    }

    public String getName() {

        return name;
    }

    public String getPrice() {
        return price;
    }

    public String getUrl() {
        return url;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public String getDescripton() {
        return descripton;
    }

    public static ArrayList<Product> getProductsFromJson(String jsonString) {
        ArrayList<Product> products = new ArrayList<>();
        try {
            JSONArray jsonArray = new JSONArray(jsonString);
            for (int i = 0; i < jsonArray.length(); ++i) {
                JSONObject jsonObject = (JSONObject) jsonArray.get(i);
                Product product = new Product();
                product.setDescripton(jsonObject.getString("description"));
                product.setImageUrl(jsonObject.getString("image_url"));
                product.setName(jsonObject.getString("name"));
                product.setPrice("$ " + jsonObject.getDouble("price"));
                product.setUrl(jsonObject.getString("url"));
                product.setAmountLeft(jsonObject.getInt("Amount") + " Left");
                products.add(product);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return products;
    }
}
