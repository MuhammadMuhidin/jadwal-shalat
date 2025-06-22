CREATE TABLE realtime_traffic_sensor (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL COMMENT 'faker.random.uuid()',
    location TEXT COMMENT 'faker.address.streetAddress()',
    plate_number VARCHAR(15) COMMENT 'faker.vehicle.vrm()',
    latitude DOUBLE PRECISION COMMENT 'faker.address.latitude()',
    longitude DOUBLE PRECISION COMMENT 'faker.address.longitude()',
    traffic_flow INTEGER COMMENT 'faker.datatype.number({ min: 0, max: 100 })',
    speed_avg DOUBLE PRECISION COMMENT 'faker.datatype.number({ min: 0, max: 120 })',
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);