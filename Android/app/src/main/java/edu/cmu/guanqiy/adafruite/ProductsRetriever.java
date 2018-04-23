package edu.cmu.guanqiy.adafruite;

import android.os.AsyncTask;
import android.util.Log;
import android.view.View;
import android.widget.ProgressBar;

import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.ref.WeakReference;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;

public class ProductsRetriever extends AsyncTask<String, Integer, ArrayList<Product>> {
    /**
     * use weak reference to prevent from holding direct reference to the MainActivity
     * which may leads to memory leaking
     */
    private WeakReference<ProgressBar> mProgressBar;

    private WeakReference<MainActivity> mActivity;

    public ProductsRetriever(MainActivity activity, ProgressBar progressBar) {
        mActivity = new WeakReference<>(activity);
        mProgressBar = new WeakReference<>(progressBar);
    }


    @Override
    protected ArrayList<Product> doInBackground(String... paramss) {
        ArrayList<Product> products = null;
        try {
            URL url = new URL("http://34.201.251.175:5000/bestsellers?limit="+paramss[0]);
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();

            InputStream stream = new BufferedInputStream(urlConnection.getInputStream());
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(stream));
            StringBuilder builder = new StringBuilder();

            String inputString;
            while ((inputString = bufferedReader.readLine()) != null) {
                builder.append(inputString);
            }

            Log.d(MainActivity.TAG, builder.toString());

            products = Product.getProductsFromJson(builder.toString());

            urlConnection.disconnect();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return products;

    }

    @Override
    protected void onPreExecute() {
        super.onPreExecute();
        final ProgressBar progressBar = mProgressBar.get();
        if (progressBar != null) {
            progressBar.setVisibility(View.VISIBLE);
        }
    }

    @Override
    protected void onPostExecute(ArrayList<Product> products) {
        super.onPostExecute(products);
        final MainActivity activity = mActivity.get();
        if (activity != null) {
            activity.onTaskCompleted(products);
        }
    }

    @Override
    protected void onProgressUpdate(Integer... values) {
        super.onProgressUpdate(values);
        final ProgressBar progressBar = mProgressBar.get();
        if (progressBar != null) {
            progressBar.setProgress(values[0]);
        }
    }
}
