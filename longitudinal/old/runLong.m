function [stats, test_names, subs, time_course] = runLong()
% function: runs the battery of longitudinal functions in the lme sequence
% 
% [stats, test_names, subs, time_course] = runLong();

%% Initialize Variables
data = [];
stats = struct;

%% Group Selection
% RAVEO
% subs = {'124_AT', '138_LA', '141_GC', '143_CH'};
% LMB
subs = {'102_RS', '110_HH', '145_AC', '150_MG', '151_RD', '152_TC', ...
        '160_EK', '161_AK', '162_EF', '163_LF', '164_SF', '170_GM', '172_TH', '174_HS', ...
        '179_GM', '180_ZD', '201_GS', '202_DD', '203_AM', '204_AM', '205_AC', '206_LM', ...
        '207_AH', '208_LH', '210_SB', '211_LB'};
        
%% Test Selection
% test_names = {'WJ_BRS'};
% test_names = {'WJ_MFF_SS', 'WJ_CALC_SS'};
test_names = {'WJ_LWID_SS', 'WJ_WA_SS', 'WJ_BRS', 'WJ_RF', 'WJ_MFF_SS',...
                'TWRE_SWE_SS', 'TWRE_PDE_SS', 'TWRE_INDEX'};
test_names = strrep(test_names, '_', '\_');
%% Time Selection
% hours = 1; days = 2; session = 3;
time_course = 3;



%% Plotting on/off
% plotting = 0 for off; 1 for on
plotting = 0;

%% Dummy coding on/off
% dummyon = 0 for off; 1 for on
dummyon = 1;




%% Gather data and perform statistics
for ii = 1:length(test_names)
   
    test_name = test_names(ii);
        
    [sid, long_var, score, test_name] = prepLongitudinaldata(data, subs, test_name, time_course);
    
    if time_course == 3
        % At least for now, maybe we just want to analyze sessions, 1, 2,
        % 3, 4. Since some subjects don't have session 0 or 5, these are a
        % bit more difficult to interpret. But let's remember to go
        % through, look at different models and understand
        usesessions = [0, 1, 2];
        indx = ismember(long_var, usesessions);
        % Here we remove rows that correspond to the ones we don't want to
        % analyze
        sid = sid(indx); long_var = long_var(indx); score = score(indx);
    end
    
    if dummyon == 0
        [lme_linear, lme_quad, data_table] = lmeLongitudinaldata(sid, long_var, score);
        stats(ii).lme_quad = lme_quad;
    elseif dummyon == 1   
        [lme_linear, data_table] = lmeCat(sid, long_var, score);
        stats(ii).sessions = long_var;
    end
    stats(ii).test_name = test_name;  
    stats(ii).lme_linear = lme_linear;
    stats(ii).data_table = data_table;  
end


%% Plot data & Lines of best fit
if plotting == 1 
    % Plot scores vs. longitudinal variable for each test of interest
    % with lines of best fit using lme stats
    [stats] = lmeLongitudinalplot(stats, test_names, subs, time_course);
    
%     if time_course ~= 3
    % Plot histogram of growth estimates with error bars
%     [stats] = lmeGrowthplot(stats, test_names, subs, time_course);
%     end
    
    % Gather by Session data and create box plots
%     [stats] = sessionPlot(stats);

elseif plotting == 0
    return;
end
return