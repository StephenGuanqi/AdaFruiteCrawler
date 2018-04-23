package edu.cmu.guanqiy.adafruite;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.util.ArrayList;

public class ProductAdapter extends BaseAdapter{

    private Context mContext;
    private LayoutInflater mInflater;
    private ArrayList<Product> mDataSource;

    public ProductAdapter(Context context, ArrayList<Product> items) {
        mContext = context;
        mDataSource = items;
        mInflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }

    @Override
    public int getCount() {
        return mDataSource.size();
    }

    @Override
    public Object getItem(int i) {
        return mDataSource.get(i);
    }

    @Override
    public long getItemId(int i) {
        return i;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        ViewHolder holder;

        if (view == null) {
            view = mInflater.inflate(R.layout.list_item_product, viewGroup, false);

            holder = new ViewHolder();
            holder.thumbnailImageView = view.findViewById(R.id.product_list_thumbnail);
            holder.priceTextView = view.findViewById(R.id.product_list_price);
            holder.descriptionTextView = view.findViewById(R.id.product_list_detail);
            holder.titleTextView = view.findViewById(R.id.product_list_title);
            holder.amountTextView = view.findViewById(R.id.product_list_amount_left);

            view.setTag(holder);
        } else {
            holder = (ViewHolder) view.getTag();
        }

        TextView titleTextView = holder.titleTextView;
        TextView descriptionTextView = holder.descriptionTextView;
        TextView priceTextView = holder.priceTextView;
        TextView amountTextView = holder.amountTextView;
        ImageView thumbnailImageView = holder.thumbnailImageView;

        Product product = mDataSource.get(i);
        titleTextView.setText(product.getName());
        descriptionTextView.setText(product.getDescripton());
        priceTextView.setText(product.getPrice());
        amountTextView.setText(product.getAmountLeft());
        Picasso.with(mContext).load(product.getImageUrl()).
                placeholder(R.mipmap.ic_launcher).into(thumbnailImageView);

        return view;
    }

    private static class ViewHolder {
        private TextView titleTextView;
        private TextView descriptionTextView;
        private TextView priceTextView;
        private TextView amountTextView;
        private ImageView thumbnailImageView;
    }
}
