<?php

namespace App\Http\Controllers;
use App\Models\Sensor;

use Illuminate\Http\Request;

class PublicDataController extends Controller
{
    public function store(Request $request){
        if($sensor = Scan::create(
            [
                'sensor_id' => $request->sensor_id,
                'measure_unit_id' => $request->measure_unit_id,
                'amount' => $request->amount
            ]
        ))        
            return response()->json($sensor, 200);
        else
            return response()->json(['error' => 'Error al guardar la información'], 500);
    }
}
