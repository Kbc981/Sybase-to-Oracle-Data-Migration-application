CREATE PROCEDURE get_employees_by_dept
    @dept_id INT
AS
BEGIN
    SELECT emp_id, emp_name, position, salary
    FROM employees
    WHERE department_id = @dept_id
END
GO
