package com.example.observerapp

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.MapView
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.MarkerOptions

class MainActivity : AppCompatActivity(), OnMapReadyCallback {

    private lateinit var mapView: MapView
    private lateinit var mMap: GoogleMap
    private lateinit var mLatLng: LatLng

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_map)

        mapView = findViewById(R.id.mapView)
        mapView.onCreate(savedInstanceState)
        mapView.getMapAsync(this)
    }

    override fun onMapReady(p0: GoogleMap) {
        mMap = p0

        var x:Double = 51.619732
        var y:Double = -3.879636
        mLatLng = LatLng(x, y)

        mMap.addMarker(MarkerOptions().position(mLatLng).title("Drone001").snippet(("This is a live drone")))

        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(mLatLng,15f))

        mMap.mapType = GoogleMap.MAP_TYPE_SATELLITE


    }
}