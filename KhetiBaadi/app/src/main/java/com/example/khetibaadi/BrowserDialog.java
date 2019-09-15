package com.example.khetibaadi;

import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import android.support.annotation.NonNull;
import android.support.annotation.Nullable;

public class BrowserDialog extends Dialog {

    private WebView browser ;

    private String search_query;

    public BrowserDialog(@NonNull Context context) {
        super(context);
    }

    public BrowserDialog(@NonNull Context context, int themeResId,String search_query) {
        super(context, themeResId);
        this.search_query = search_query;
    }

    public BrowserDialog(@NonNull Context context, boolean cancelable, @Nullable OnCancelListener cancelListener) {
        super(context, cancelable, cancelListener);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.dialog_browser);
        browser = findViewById(R.id.browser);

        browser.loadUrl("https://www.google.com/search?q=" + search_query);
        browser.setWebViewClient(new WebViewClient(){
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });
        browser.getSettings().setJavaScriptEnabled(true);
    }

    @Override
    public void onBackPressed() {
        if(browser.canGoBack())
            browser.goBack();
        else
            super.onBackPressed();
    }
}