package com.example.khetibaadi


import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.support.v7.app.AppCompatActivity

class SplashActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)
        Handler().postDelayed({
            val homeIntent = Intent(this@SplashActivity, MainActivity::class.java)
            startActivity(homeIntent)
            finish()
        }, 2000)
    }
}
