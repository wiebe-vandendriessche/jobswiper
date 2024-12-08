package org.example;

import java.util.Optional;


public class Salary {

    private double min;
    private double max;

    public Salary() {
        this.min = 0;
        this.max = 300000;
    }


    public Salary(double min, double max) {
        if (min > max) {
            throw new IllegalArgumentException("Minimum salary cannot be greater than maximum salary.");
        }
        this.min = min;
        this.max = max;
    }


    public void updateSalaryRange(Optional<Double> min, Optional<Double> max) {

        if (min.isPresent()) {
            if (max.isPresent() && min.get() > max.get()) {
                throw new IllegalArgumentException("Minimum salary cannot be greater than maximum salary.");
            }
            this.min = min.get();
        }


        if (max.isPresent()) {
            if (min.isPresent() && max.get() < min.get()) {
                throw new IllegalArgumentException("Maximum salary cannot be less than minimum salary.");
            }
            this.max = max.get();
        }
    }


    public double getMin() {
        return min;
    }

    public void setMin(double min) {
        if (min > this.max) {
            throw new IllegalArgumentException("Minimum salary cannot be greater than maximum salary.");
        }
        this.min = min;
    }

    public double getMax() {
        return max;
    }

    public void setMax(double max) {
        if (max < this.min) {
            throw new IllegalArgumentException("Maximum salary cannot be less than minimum salary.");
        }
        this.max = max;
    }

    @Override
    public String toString() {
        return String.format("Salary(min=%.2f$, max=%.2f$)", min, max);
    }

}
