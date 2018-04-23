package edu.cmu.guanqiy.adafruite;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.ProgressBar;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private ListView mListView;
    private ProgressBar mProgressBar;
    private ArrayList<Product> mProducts;
    private static final int numToGet = 20;

    public static final String TAG = MainActivity.class.getSimpleName();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final Context context = this;

        mProgressBar = findViewById(R.id.progressBar);
        mProgressBar.setMax(10);
        mProgressBar.setVisibility(View.INVISIBLE);

        // Create list view
        mListView = findViewById(R.id.products_list_view);

        // Set what happens when a list view item is clicked
        mListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Product selectedProduct = mProducts.get(position);

                Intent detailIntent = new Intent(context, ProductDetailActivity.class);
                detailIntent.putExtra("title", selectedProduct.getName());
                detailIntent.putExtra("url", selectedProduct.getUrl());

                startActivity(detailIntent);
            }

        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        new ProductsRetriever(this, mProgressBar).execute("" + numToGet);
    }

    public void onTaskCompleted(ArrayList<Product> products) {
        mProgressBar.setVisibility(View.INVISIBLE);
        mProducts = products;

        // Create adapter
        ProductAdapter adapter = new ProductAdapter(this, mProducts);
        mListView.setAdapter(adapter);

        mListView.invalidate();
    }
}
