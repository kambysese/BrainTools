function [stats] = lmeGrowthplot(stats, test_names, subs, time_course)
% [stats] = lmeGrowthplot(stats, test_names, subs, time_course)
% 
% Function: plots histogram of growth statistics of lme data
% Inputs: stats, type struct; test_names; subs; time_course
% Outputs: figure, type histogram
% Example:

%% Variables
% Number of statistics gathered
% growth estimate; standard error
num_stats = 3;


%% Linear
figure; hold;

for ii = 1:length(test_names)
    linear_data(ii,:) = table(test_names(ii), stats(ii).lme.Coefficients.Estimate(2), stats(ii).lme.Coefficients.SE(2));
    linear_data.Properties.VariableNames = {'test_name', 'Growth', 'SE'};
end
   h = bar(linear_data.Growth, 'FaceColor', 'g', 'EdgeColor', 'k');
   errorbar(linear_data.Growth, linear_data.SE);

% Format
ylabel('Growth Estimate'); xlabel('Test Name');
ax = gca;
ax.XTick = 1:length(test_names);
ax.XTickLabel = test_names;
title('Linear Growth Estimate by Test');

for ii = 1:length(test_names)
    text(ii-.25, 0.02, num2str(stats(ii).lme.Coefficients.pValue(2)))
end



%% Quadratic
figure; hold;

for ii = 1:length(test_names)
    quad_data(ii,:) = table(test_names(ii), stats(ii).lme2.Coefficients.Estimate(3), stats(ii).lme2.Coefficients.SE(3));
    quad_data.Properties.VariableNames = {'test_name', 'Growth', 'SE'};
end
   h = bar(quad_data.Growth, 'FaceColor', 'g', 'EdgeColor', 'k');
   errorbar(quad_data.Growth, linear_data.SE);

% Format
ylabel('Growth Estimate'); xlabel('Test Name');
ax = gca;
ax.XTick = 1:length(test_names);
ax.XTickLabel = test_names;
title('Quadratic Growth Estimate by Test');

% Add p values
for ii = 1:length(test_names)
    text(ii-.25, 0.02, num2str(stats(ii).lme2.Coefficients.pValue(3)))
end

    

        

end