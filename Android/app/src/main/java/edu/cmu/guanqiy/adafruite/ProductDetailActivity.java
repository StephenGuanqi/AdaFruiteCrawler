package edu.cmu.guanqiy.adafruite;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.webkit.WebView;

public class ProductDetailActivity extends AppCompatActivity {

    private WebView mWebView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_product_detail);

        // Get recipe data passed from previous activity
        String title = this.getIntent().getExtras().getString("title");
        String url = this.getIntent().getExtras().getString("url");

        // Set title on action bar of this activity
        setTitle(title);

        // Create WebView and load web page
        mWebView = findViewById(R.id.detail_web_view);
        mWebView.loadUrl(url);
    }

}
