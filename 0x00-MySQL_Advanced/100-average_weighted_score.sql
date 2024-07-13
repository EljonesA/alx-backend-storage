-- Stored procedure that computes and store the average weighted score for a student.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
    
    -- Calculate the total weighted score
    SELECT SUM(c.score * p.weight)
    INTO total_weighted_score
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- Calculate the total weight
    SELECT SUM(p.weight)
    INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- Update the average_score for the user
    UPDATE users
    SET average_score = (CASE 
                            WHEN total_weight = 0 THEN 0 
                            ELSE total_weighted_score / total_weight 
                         END)
    WHERE id = user_id;
END //

DELIMITER ;
