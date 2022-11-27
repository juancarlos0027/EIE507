<?php

namespace App\Http\Controllers;
use App\Models\Sensor;

use Illuminate\Http\Request;

class PublicDataController extends Controller
{
    public function store(Request $request){
        if($sensor = Scan::create($request->all()))
            return response()->json($sensor, 200);
        else
            return response()->json(['error' => 'Error al guardar la información'], 500);
    }
}
