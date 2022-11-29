<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Scan extends Model
{
    use HasFactory;

    protected $fillable = [
        'sensor_id',
        'measure_unit_id',
        'amount'
    ];

    protected $cast = [
        'created_at' => 'datetime:d-m-Y H:i:s',
    ];
}
