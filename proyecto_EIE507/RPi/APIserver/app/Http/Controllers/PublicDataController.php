<?php

namespace App\Http\Controllers;
use App\Models\Sensor;

use Illuminate\Http\Request;

class PublicDataController extends Controller
{
    public function store(Request $request){
        //$request is a JSON object, so we need to decode it
        $data = json_decode($request->getContent(), true);

        if($sensor = Scan::create(
            [
                'sensor_id' => $data->sensor_id,
                'measure_unit_id' => $data->measure_unit_id,
                'amount' => $data->amount
            ]
        ))        
            return response()->json($sensor, 200);
        else
            return response()->json(['error' => 'Error al guardar la información'], 500);
    }
}
